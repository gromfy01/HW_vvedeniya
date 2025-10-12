# Инструкция по развёртыванию кластера YARN

## Предпосылки
- Кластер HDFS (из ДЗ 1) уже развёрнут и работает
- 4 ВМ с Ubuntu 24.04, Python 3.12.3, Java 11.0.26
- Пользователь `team` с sudo правами
- Сетевые адреса: 192.168.1.35-38

## Быстрая установка

1. **Подключитесь к jump-ноде:**
```bash
ssh team@176.109.91.44
Клонируйте репозиторий:

bash
git clone https://github.com/gromfy01/HW_vvedeniya.git
cd HW_vvedeniya/hw2
Запустите подготовительный скрипт:

bash
bash ./prepare.sh
Введите пароль пользователя team: 8tdxAQ-nov

Запустите развёртывание YARN:

bash
cd ansible
ansible-playbook -i inventory.ini create_yarn_cluster.yml --ask-become-pass
Введите пароль пользователя team при запросе.

Проверка установки
Проверка сервисов
bash
# На ResourceManager узле (192.168.1.35)
systemctl status hadoop-resourcemanager
/opt/hadoop/bin/yarn node -list  # Должны быть 3 NodeManager

# На NodeManager узлах
systemctl status hadoop-nodemanager

# На HistoryServer узле
systemctl status hadoop-historyserver
Тестовая MR задача
bash
/opt/hadoop/bin/hadoop jar \
  /opt/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar \
  pi 2 100
Доступ к веб-интерфейсам
На локальной машине выполните:

bash
# ResourceManager UI
ssh -L 8088:192.168.1.35:8088 team@176.109.91.44

# NodeManager UI (для любого NM)
ssh -L 8042:192.168.1.36:8042 team@176.109.91.44

# JobHistory UI
ssh -L 19888:192.168.1.35:19888 team@176.109.91.44

# Web App Proxy
ssh -L 9099:192.168.1.35:9099 team@176.109.91.44
Откройте в браузере:

ResourceManager: http://localhost:8088

NodeManager: http://localhost:8042

JobHistory: http://localhost:19888

Web Proxy: http://localhost:9099

Порты сервисов
ResourceManager Web UI: 8088

NodeManager Web UI: 8042

JobHistory Web UI: 19888

Web App Proxy: 9099

Структура репозитория
text
hw2/
├── Instruction.md
├── prepare.sh
└── ansible/
    ├── inventory.ini
    ├── group_vars/
    │   └── all.yml
    ├── roles/
    │   ├── common/
    │   │   └── tasks/
    │   │       └── main.yml
    │   ├── hadoop/
    │   │   └── tasks/
    │   │       └── main.yml
    │   └── yarn/
    │       ├── tasks/
    │       │   └── main.yml
    │       ├── templates/
    │       │   ├── core-site.xml.j2
    │       │   ├── yarn-site.xml.j2
    │       │   ├── mapred-site.xml.j2
    │       │   ├── hadoop-env.sh.j2
    │       │   ├── resourcemanager.service.j2
    │       │   ├── nodemanager.service.j2
    │       │   ├── historyserver.service.j2
    │       │   └── proxyserver.service.j2
    │       └── files/
    │           └── profile.d/
    │               └── hadoop.sh
    └── create_yarn_cluster.yml
