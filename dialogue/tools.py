import os
import time
import logging
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def log_operator(level: str, log_file: str = None,
                 log_format: str = "[%(levelname)s] - [%(asctime)s] - [file: %(filename)s] - "
                                   "[function: %(funcName)s] - [%(message)s]") -> logging.Logger:
    """ 日志操作方法，日志级别有'CRITICAL','FATAL','ERROR','WARN','WARNING','INFO','DEBUG','NOTSET'
    CRITICAL = 50, FATAL = CRITICAL, ERROR = 40, WARNING = 30, WARN = WARNING, INFO = 20, DEBUG = 10, NOTSET = 0

    :param log_file: 日志路径
    :param level: 日志级别
    :param log_format: 日志信息格式
    :return: 日志记录器
    """
    if log_file is None:
        log_file = os.path.abspath(__file__)[
                   :os.path.abspath(__file__).rfind("\\dialogue\\")] + '\\dialogue\\data\\preprocess\\runtime.log'

    logger = logging.getLogger()
    logger.setLevel(level)
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(level=level)
    formatter = logging.Formatter(log_format)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def show_history(self, history, save_dir, valid_freq):
    """ 用于显示历史指标趋势以及保存历史指标图表图

    :param history: 历史指标
    :param save_dir: 历史指标显示图片保存位置
    :param valid_freq: 验证频率
    :return: 无返回值
    """
    train_x_axis = [i + 1 for i in range(len(history['loss']))]
    valid_x_axis = [(i + 1) * valid_freq for i in range(len(history['val_loss']))]

    figure, axis = plt.subplots(1, 1)
    tick_spacing = 1
    if len(history['loss']) > 20:
        tick_spacing = len(history['loss']) // 20
    plt.plot(train_x_axis, history['loss'], label='loss', marker='.')
    plt.plot(train_x_axis, history['accuracy'], label='accuracy', marker='.')
    plt.plot(valid_x_axis, history['val_loss'], label='val_loss', marker='.', linestyle='--')
    plt.plot(valid_x_axis, history['val_accuracy'], label='val_accuracy', marker='.', linestyle='--')
    plt.xticks(valid_x_axis)
    plt.xlabel('epoch')
    plt.legend()

    axis.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

    save_path = save_dir + time.strftime("%Y_%m_%d_%H_%M_%S_", time.localtime(time.time()))
    if not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)
    plt.savefig(save_path)
    plt.show()