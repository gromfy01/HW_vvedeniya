# Инструкция по развёртыванию кластера YARN

Инструкция hw2 выполняются при условии, что выполнены шаги инструкции hw1


1. **Все действия выполняем на jn ноде**
```bash
ssh team@176.109.91.44
```

2. **Склонировать github репозиторий**
```bash
git clone https://github.com/gromfy01/HW_vvedeniya.git
```

3. **Перейти в директорию hw2/**
```bash
cd HW_vvedeniya/hw2
```

4. **Перейти в поддиректорию ansible/**
```bash
cd ansible
```

5. **Запустить Ansible playbook и на запрос ввести пароль пользователя team**
```bash
ansible-playbook -i inventory.ini create_yarn_cluster.yml --ask-become-pass
```

Он разворачивает кластер YARN и выполняет проверки корректности установки.

6. **Запустить ssh туннели и проверить доступность web-интерфейсов**

Для ResourceManager:
```bash
ssh -L 8088:192.168.1.35:8088 team@176.109.91.44
```
После этого в браузере откройте: [http://localhost:8088/](http://localhost:8088/)

Для NodeManager:
```bash
ssh -L 8042:192.168.1.35:8042 team@176.109.91.44
```
После этого в браузере откройте: [http://localhost:8042/](http://localhost:8042/)

Для HistoryServer:
```bash
ssh -L 19888:192.168.1.35:19888 team@176.109.91.44
```
После этого в браузере откройте: [http://localhost:19888/](http://localhost:19888/)

```
Структура репозитория
```bash
hw2/
├── Instruction.md
└── ansible/
    ├── inventory.ini
    ├── group_vars/
    │   └── all.yml
    ├── roles/
    │   └── yarn/
    │       ├── tasks/
    │       │   └── main.yml
    │       ├── templates/
    │       │   ├── yarn-site.xml.j2
    │       │   └── mapred-site.xml.j2
    │       └── files/
    └── create_yarn_cluster.yml
```
