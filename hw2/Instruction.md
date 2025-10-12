```markdown
# Инструкция по развёртыванию кластера YARN

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
ansible-playbook -i inventory.ini create_yarn_cluster.yml --ask-become-pass
```

Он разворачивает кластер YARN и выполняет проверки корректности установки.

7. **Запустить ssh туннели и проверить доступность web-интерфейсов**

Для ResourceManager:
```bash
ssh -L 8088:192.168.1.35:8088 team@176.109.91.44
```
После этого в браузере откройте: [http://localhost:8088/](http://localhost:8088/)

Для NodeManager:
```bash
ssh -L 8042:192.168.1.36:8042 team@176.109.91.44
```
После этого в браузере откройте: [http://localhost:8042/](http://localhost:8042/)

Для JobHistory:
```bash
ssh -L 19888:192.168.1.35:19888 team@176.109.91.44
```
После этого в браузере откройте: [http://localhost:19888/](http://localhost:19888/)

Для Web Proxy:
```bash
ssh -L 9099:192.168.1.35:9099 team@176.109.91.44
```
После этого в браузере откройте: [http://localhost:9099/](http://localhost:9099/)
```

Чтобы обновить файл, выполни:

```bash
cat > hw2/Instruction.md << 'EOF'
# Инструкция по развёртыванию кластера YARN

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
ansible-playbook -i inventory.ini create_yarn_cluster.yml --ask-become-pass
```

Он разворачивает кластер YARN и выполняет проверки корректности установки.

7. **Запустить ssh туннели и проверить доступность web-интерфейсов**

Для ResourceManager:
```bash
ssh -L 8088:192.168.1.35:8088 team@176.109.91.44
```
После этого в браузере откройте: [http://localhost:8088/](http://localhost:8088/)

Для NodeManager:
```bash
ssh -L 8042:192.168.1.36:8042 team@176.109.91.44
```
После этого в браузере откройте: [http://localhost:8042/](http://localhost:8042/)

Для JobHistory:
```bash
ssh -L 19888:192.168.1.35:19888 team@176.109.91.44
```
После этого в браузере откройте: [http://localhost:19888/](http://localhost:19888/)

Для Web Proxy:
```bash
ssh -L 9099:192.168.1.35:9099 team@176.109.91.44
```
После этого в браузере откройте: [http://localhost:9099/](http://localhost:9099/)
