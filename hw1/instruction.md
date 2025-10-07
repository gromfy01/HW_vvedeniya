# Инструкция по развёртыванию кластера HDFS

1. **Все действия выполняем на jn ноде**
```bash
ssh team@176.109.91.44
```

2. **Склонировать github репозиторий**
```bash
git clone git@github.com:gromfy01/HW_vvedeniya.git
```

3. **Перейти в директорию hw1/**
```bash
cd HW_vvedeniya/hw1
```

4. **Запустить Bash-script и на запрос ввести пароль пользователя team**
```bash
bash ./prepare.sh
```

Он устанавливает Ansible, sshpass, затем генерирует ssh-ключи и раскладывает их по нодам.

5. **Перейти в поддиректорию ansible/**
```bash
cd ansible
```

6. **Запустить Ansible playbook и на запрос ввести пароль пользователя team**
```bash
ansible-playbook -i inventory.ini  create_hadoop_cluster.yml  --ask-become-pass
```

Он разворачивает кластер HDFS и выполняет проверки корректности установки.

7. **Запустить ssh туннель и проверить доступность web-интерфейса**
```bash
ssh -L 9870:192.168.1.35:9870 team@176.109.91.44
```

После этого в браузере откройте: [http://localhost:9870/](http://localhost:9870/)
