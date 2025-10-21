# Инструкция по развёртыванию кластера Hive

Инструкция hw3 выполняются при условии, что выполнены шаги инструкций hw1 и hw2


1. **Все действия выполняем на jn ноде**
```bash
ssh team@176.109.91.44
```

2. **Склонировать github репозиторий**
```bash
git clone https://github.com/gromfy01/HW_vvedeniya.git
```

3. **Перейти в директорию hw3/**
```bash
cd HW_vvedeniya/hw3
```

4. **Перейти в поддиректорию ansible/**
```bash
cd ansible
```

5. **Запустить Ansible playbook и на запрос ввести пароль пользователя team**
```bash
ansible-playbook -i inventory.ini install_configure_hive.yml --ask-become-pass
```

Он разворачивает hive, выполняет проверки корректности установки, загружает датасет и создаёт таблицы. 

6. **Запустить ssh туннели и проверить доступность web-интерфейсов**

```bash
ssh -L 10020:nn:/10020 -L 9870:nn:9870 -L 8088:nn:8088  -L 19888:nn:19888 team@176.109.91.44
```
После этого в браузере откройте: [http://localhost:10002/](http://localhost:10002/)

Структура репозитория

```bash
hw3/
├── Instruction.md
└── ansible/
    ├── inventory.ini    
    ├── roles/
    │   │
    │   ├── hive/
    │   │   ├── tasks/
    │   │   │   └── main.yml
    │   │   └── templates/
    │   │       └── hive-site.xml.j2 
    │   └── postgres/
    │       └── tasks/
    │           └── main.yml       
    ├── files/
    └── install_configure_hive.yml
```
