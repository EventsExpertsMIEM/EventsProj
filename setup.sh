export PGUSER=""
# адрес postgresql
export PGHOST="127.0.0.1"
# порт postgresql
export PGPORT="5432"
# название БД в postgresql
export PGDATABASE="congress_events"
# пароль пользователя postgresql
export PGPASSWORD=""

# порт приложения
export PORT="4000"

# почта супер-администратора
export SUPER_ADMIN_MAIL=""
# пароль от аккаунта супер-админа
export SUPER_ADMIN_PASSWORD=""
# подтверждение регистрации по электронной почте # 'active' (account_status) для отключения подтверждения # 'unconfirmed' (account_status) для включения
export DEFAULT_USER_STATUS="active"

# временно - линк на сервис (http(s)://адрес:порт)
export SITE_ADDR="congressevents.com"

# Уровень логгирования
export LOG_LEVEL=0
# Отключать ли сторонние логгеры
export DISABLE_EXISTING_LOGGERS=True

# SMTP сервер
export MAIL_SERVER=""
# Порт на почтовом сервере
export MAIL_PORT=25
# Логин для почтового сервера
export MAIL_USERNAME=""
# Пароль от почтового сервера
export MAIL_PASSWORD=""
# Адрес, который будет указан в поле From
export MAIL_DEFAULT_SENDER="noreply@$SITE_ADDR"

# Корневая папка для хранения загруженный файлов
export FILE_UPLOADS_PARENT_FOLDER=""
# Максимальный размер файла (пока только в Мб)
export MAX_FILE_SIZE=100
