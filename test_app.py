import pytest
import json
from unittest.mock import patch, MagicMock
from app import app, validate_input, validate_email, sanitize_input, generate_token


@pytest.fixture
def client():
    """建立測試客戶端"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_page(client):
    """測試首頁是否正常顯示"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'CustomizeGPT' in response.data


def test_login_page(client):
    """測試登入頁面是否正常顯示"""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'CustomizeGPT' in response.data


def test_validate_input_success():
    """測試輸入驗證 - 成功案例"""
    data = {'account': 'test@example.com', 'password': 'password123'}
    is_valid, error = validate_input(data, ['account', 'password'])
    assert is_valid is True
    assert error is None


def test_validate_input_missing_field():
    """測試輸入驗證 - 缺少欄位"""
    data = {'account': 'test@example.com'}
    is_valid, error = validate_input(data, ['account', 'password'])
    assert is_valid is False
    assert '缺少必要欄位' in error


def test_validate_input_empty_value():
    """測試輸入驗證 - 空值"""
    data = {'account': '', 'password': 'password123'}
    is_valid, error = validate_input(data, ['account', 'password'])
    assert is_valid is False


def test_validate_input_too_long():
    """測試輸入驗證 - 超過長度限制"""
    data = {'account': 'a' * 300, 'password': 'password123'}
    is_valid, error = validate_input(data, ['account', 'password'])
    assert is_valid is False
    assert '超過長度限制' in error


def test_validate_email_valid():
    """測試電子郵件驗證 - 有效郵件"""
    assert validate_email('test@example.com') is True
    assert validate_email('user.name+tag@example.co.uk') is True


def test_validate_email_invalid():
    """測試電子郵件驗證 - 無效郵件"""
    assert validate_email('invalid-email') is False
    assert validate_email('@example.com') is False
    assert validate_email('test@') is False


def test_sanitize_input():
    """測試輸入清理"""
    assert sanitize_input('  test  ') == 'test'
    assert sanitize_input('test') == 'test'
    assert sanitize_input(123) == ''


def test_generate_token():
    """測試 token 產生"""
    token1 = generate_token()
    token2 = generate_token()

    assert len(token1) > 0
    assert len(token2) > 0
    assert token1 != token2  # 每次應該產生不同的 token


@patch('app.readAccount')
@patch('app.updateAccount')
def test_login_action_success(mock_update, mock_read, client):
    """測試登入 - 成功案例"""
    mock_read.return_value = {'account': 'test@example.com'}
    mock_update.return_value = {'status': 'success'}

    response = client.post('/login-action',
                          data=json.dumps({
                              'account': 'test@example.com',
                              'password': 'password123'
                          }),
                          content_type='application/json')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert 'token' in data


@patch('app.readAccount')
def test_login_action_invalid_credentials(mock_read, client):
    """測試登入 - 帳號密碼錯誤"""
    mock_read.return_value = None

    response = client.post('/login-action',
                          data=json.dumps({
                              'account': 'test@example.com',
                              'password': 'wrongpassword'
                          }),
                          content_type='application/json')

    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['status'] == 'error'


def test_login_action_missing_data(client):
    """測試登入 - 缺少必要資料"""
    response = client.post('/login-action',
                          data=json.dumps({
                              'account': 'test@example.com'
                          }),
                          content_type='application/json')

    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['status'] == 'error'


def test_login_action_invalid_email(client):
    """測試登入 - 無效的電子郵件格式"""
    response = client.post('/login-action',
                          data=json.dumps({
                              'account': 'invalid-email',
                              'password': 'password123'
                          }),
                          content_type='application/json')

    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['status'] == 'error'
    assert '電子郵件格式不正確' in data['message']


@patch('app.calln8n')
def test_call_ai_success(mock_calln8n, client):
    """測試 AI 呼叫 - 成功案例"""
    mock_calln8n.return_value = {'output': 'AI response'}

    response = client.get('/callAI?message=test message')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'AI response'


def test_call_ai_empty_message(client):
    """測試 AI 呼叫 - 空訊息"""
    response = client.get('/callAI?message=')

    assert response.status_code == 400
    data = json.loads(response.data)
    assert '請輸入訊息' in data['message']


def test_call_ai_too_long_message(client):
    """測試 AI 呼叫 - 訊息過長"""
    long_message = 'a' * 5001
    response = client.get(f'/callAI?message={long_message}')

    assert response.status_code == 400
    data = json.loads(response.data)
    assert '訊息過長' in data['message']


@patch('app.calln8n')
def test_call_ai_service_failure(mock_calln8n, client):
    """測試 AI 呼叫 - 服務失敗"""
    mock_calln8n.return_value = None

    response = client.get('/callAI?message=test')

    assert response.status_code == 503
    data = json.loads(response.data)
    assert 'AI 服務暫時無法回應' in data['message']


def test_404_error(client):
    """測試 404 錯誤處理"""
    response = client.get('/nonexistent-page')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['status'] == 'error'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
