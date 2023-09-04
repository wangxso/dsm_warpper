
from flask import Flask
from routes.filestation import fs_bp
from routes.system import sys_bp
from loguru import logger
import logging

app = Flask(__name__)
# 移除默认的日志处理器
app.logger.handlers = []

logger.add("app.log", rotation="500 MB", level="DEBUG", enqueue=True)

# 创建一个适配器，将 Loguru 日志记录器包装为 Flask 的日志记录器接口
class LoguruAdapter(logging.LoggerAdapter):
    def __init__(self, logger):
        super().__init__(logger, {})

    def process(self, msg, kwargs):
        self.extra.update(kwargs)
        return msg, self.extra

# 创建 LoguruAdapter 实例，将 Loguru 的 logger 传递给它
app.logger = LoguruAdapter(logger)
app.register_blueprint(fs_bp)
app.register_blueprint(sys_bp)


if __name__ == "__main__":
    host = '127.0.0.1'
    port = 5000
    with app.app_context():
        routes = [str(rule) for rule in app.url_map.iter_rules()]
        for route in routes:
            logger.info(f'http://{host}:{port}{route}')
    app.run(host=host, port=port, debug=True)