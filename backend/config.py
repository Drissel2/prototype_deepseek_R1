import os

class Settings:
    # احصل على قيمة PORT من البيئة، وتأكد أنها رقم صحيح
    port_str = os.getenv('PORT')
    if port_str and port_str.isdigit():
        PORT: int = int(port_str)
    else:
        PORT: int = 5000

    # يمكن إضافة إعدادات أخرى هنا حسب حاجتك
    DEBUG: bool = bool(os.getenv('DEBUG', 'False').lower() in ['true', '1', 'yes'])
    # مثلاً إعدادات أخرى
    MODEL_PATH = os.getenv('MODEL_PATH', './model')
    
settings = Settings()
