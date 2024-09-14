import unittest
from app import app, db, Movie, User


class WatchlistTestCase(unittest.TestCase):
    
    def setUp(self):
        # 更新配置
        app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'
        )
        
        with app.app_context():
            # 创建数据库和表
            db.create_all()
            # 创建测试数据，一个用户，一个电影条目
            user = User(name='Test', username='test')
            user.set_password('123')
            movie = Movie(title='Test Movie Title', year='2019')
            # 使用 add_all() 方法一次添加多个模型类实例，传入列表
            db.session.add_all([user, movie])
            db.session.commit()

        self.client = app.test_client()  # 创建测试客户端
        self.runner = app.test_cli_runner()  # 创建测试命令运行器

    def tearDown(self):
        db.session.remove()  # 清除数据库会话
        db.drop_all()  # 删除数据库表
        
    # 测试程序实例是否存在
    def test_app_exist(self):
        self.assertIsNotNone(app)
        
    # 测试程序是否处于测试模式
    def test_app_is_testing(self):
        self.assertTrue(app.config['TESTING'])
        
    # 辅助方法，用于登入用户
    def login(self):
        self.client.post('/login', data=dict(
            username='test',
            password='123'
        ), follow_redirects=True)
        
    """
    app.test_client() 返回一个测试客户端对象，可以用来模拟客户端（浏览器），我们创建类属性 self.client 来保存它。
    对它调用 get() 方法就相当于浏览器向服务器发送 GET 请求，调用 post() 则相当于浏览器向服务器发送 POST 请求，以此类推。
    下面是两个发送 GET 请求的测试方法，分别测试 404 页面和主页：
    """
    
    # 测试404页面
    def test_404_page(self):
        response = self.client.get('/nothing')  # 发送请求
        data = response.get_data(as_text=True)  # 获取响应数据
        self.assertIn('Page Not Found', data)
        self.assertIn('Go Back', data)
        self.assertEqual(response.status_code, 404)  # 检查响应状态码
        
    # 测试主页
    def test_index_page(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)  # 获取响应数据
        self.assertIn("Test's Watchlist", data)  # 检查是否包含正确的页面元素
        self.assertIn('Test Movie Title', data)
        self.assertEqual(response.status_code, 200)  # 检查响应状态码
        
        
if __name__ == '__main__':
    unittest.main()
            