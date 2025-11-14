# SQL Blocks
Open-source инструмент для борьбы с дублированием SQL-кода через композицию переиспользуемых блоков.

## Проблема

При работе со сложными аналитическими запросами часто возникают одинаковые CTE (Common Table Expressions), которые копируются между разными SQL-файлами. Это приводит к:
- дублированию кода
- сложностям при изменении логики
- ошибкам синхронизации

## Решение

SQL Blocks Assembler позволяет декомпозировать SQL-запросы на переиспользуемые блоки с системой зависимостей. 

### Ключевые возможности

- **📦 Модульность** - разбивайте запросы на логические блоки
- **🔄 Переиспользование** - используйте одни и те же блоки в разных запросах  
- **📐 Зависимости** - автоматическое разрешение порядка выполнения через граф зависимостей

## Быстрый старт

### Установка

```bash
git clone <repository-url>
cd sqlblocks
```
### Пример использования
#### 1. Создайте SQL блоки в файлах
blocks/users.sql
```sql
SELECT 
    id,
    name,
    email
FROM users 
WHERE active = true
```
blocks/sales.sql
```sql
SELECT
    u.name,
    s.amount,
    s.date
FROM monthly_sales s
JOIN users u ON s.user_id = u.id  -- зависит от блока 'users'
```
#### 2. Используйте в коде:

```python
from sqlblocks import BasicSQLBlock, SQLBlockRegistry, SQLAssembler
from sqlblocks.plugins.folder_plugin import FolderPlugin
from pathlib import Path

# 1. Инициализация
registry = SQLBlockRegistry()
plugin = FolderPlugin('/path/to/sql/blocks')
registry = SQLBlockRegistry()
sqlassembly = SQLAssembler(registry, plugin)

# 2. Инициализация SQL блоков
registry.add_block(BasicSQLBlock(
    name="users",
    depends=None,
    source="users.sql",
))
registry.add_block(BasicSQLBlock(
    name="sales",
    depends=("users",),
    source="sales.sql",
))

# 3. Компиляция 
query = sqlassembly.assemble_sql("main_block")
```
#### Результат
```sql
WITH
users AS (
    SELECT 
        id,
        name,
        email
    FROM users 
    WHERE active = true
)
SELECT
    u.name,
    s.amount,
    s.date
FROM sales s
JOIN users u ON s.user_id = u.id
```

## Архитектура

Основные компоненты
- **SQLBlock** - модель блока с зависимостями
- **SQLBlockRegistry** - реестр для управления блоками
- **SQLAssembler** - ядро для сборки запросов
- **Плагины** - система загрузки блоков

## Поддерживаемые плагины

- **✅ FolderPlugin** - загрузка из файловой системы
- **🔄 In progress:** БД, REST API, словари

## Текущий статус

**🚧 Активная разработка** - проект в стадии альфа-тестирования. Основной функционал работает, API может меняться.

Вклад в разработку

Любые предложения и pull requests приветствуются!

## Лицензия

📄 **MIT License** - свободная лицензия с минимальными ограничениями.  
Разрешает использование, модификацию и распространение кода в коммерческих и некоммерческих целях.

Полный текст лицензии доступен в файле [LICENSE](LICENSE).