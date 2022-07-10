# **Multinode Cluster Spark**
![](https://www.researchgate.net/publication/355952131/figure/fig1/AS:1086966133207040@1636164329587/A-typical-Spark-cluster-architecture.png)


Para conseguirmos realizar as atividades do curso da Data Science Academy precisamos criar um **Multinode Cluster Spark de Teste**, para isto iremos seguir os passos abaixo para realizar as configurações necessárias para a execução das atividades.

>Como alternativa ao uso do Virtual Box poderiamos criar o cluster na AWS com o uso do EC2. Para isso podemos seguir os passos a partir da configuração do Java JDK 1.8 e o Apache Spark..


Para a configuração deste Multinode Cluster Spark de Exemplo iremos utilizar os seguintes itens:
 
 * **Oracle Virtual Box**
 * **CentOS (Minimal ISO)**
 * **Java JDK (1.8)**
 * **Apache Spark**


# Instalando o Sistema Operacional CentOS nas Virtual Machine
#### Para a criação da VM é só realizar as configurações conforme imagens abaixo.

![](/dsa-ml-ia-ambientes-distribuidos/02_configurando_multinode_spark/imgs/etapa-1-config-vm.PNG)

#### Escolher o tamanho da memória ram da VM, conforme imagem abaixo.

>Para a configuração de memória ram dos nós do cluster Spark, utilizar metade do máximo de ram e distribuir entre os nós do cluster. Como exemplo, digamos que tenhamos na nossa máquina 16 GB de RAM utilizaremos 4 GB para o SparkMaster e 2 GB para cada um dos SparkSlaves.

![](/dsa-ml-ia-ambientes-distribuidos/02_configurando_multinode_spark/imgs/etapa-2-config-vm.PNG)

#### Escolher a opção "Criar um novo disco rígido virtual agora", conforme imagem abaixo.

![](/dsa-ml-ia-ambientes-distribuidos/02_configurando_multinode_spark/imgs/etapa-3-config-vm.PNG)

#### Escolher a opção "VMDK (Virtual Machine Disk), conforme imagem abaixo.

![](/dsa-ml-ia-ambientes-distribuidos/02_configurando_multinode_spark/imgs/etapa-4-config-vm.PNG)

#### Escolher a opção "Dinammicamente alocado", conforme imagem abaixo.

![](/dsa-ml-ia-ambientes-distribuidos/02_configurando_multinode_spark/imgs/etapa-5-config-vm.PNG)

#### Escolher o tamanho em GB do disco, conforme imagem abaixo.

>Para a configuração de memória de armazenamento dos nós do cluster Spark, utilizar 64 GB.

![](/dsa-ml-ia-ambientes-distribuidos/02_configurando_multinode_spark/imgs/etapa-6-config-vm.PNG)

# Configurando o SUDOERS e o SSH para acesso aos nós do Cluster via Putty
>**Observação:**
>
>As configurações abaixo devem serem realizadas em todos os nós do cluster Spark.

#### Acessar o computador como usuário **root**.
~~~
su - root
~~~

#### Executar os comandos abaixo para realizar a instalação e configuração do **openssh-server**.

~~~
# Instalar o opensssh-server
yum install -y openssh-server

# Inicializar o serviço sshd
systemctl start sshd
~~~

#### Executar os comandos abaixo para realizar a configuração do **sudoers** para os usuários criados durante a instalação.
~~~
# Embaixo do "Allow root to run any commands anywhere" colocar o usuário criado conforme a configuração do root.
vi /etc/sudoers
~~~

# Instalando e Configurando o Java JDK
>**Observação:**
>
> A instalação e configuração do Java JDK 1.8, abaixo, deve ser realizado em todos os nós do cluster Spark como usuário aluno.

#### Acessar a pasta opt para realizar a instalação do **Java JDK 1.8**.
~~~
cd /opt
~~~

#### Instalar o pacote **wget**.
~~~
sudo yum install -y wget
~~~

#### Fazer o download do **Java JDK 1.8**.
~~~
sudo wget http://datascienceacademy.com.br/blog/aluno/JDK/jdk-8u181-linux-x64.tar.gz
~~~

#### Descompactar o **TARBALL** do **Java JDK 1.8** arquivo.
~~~
sudo tar xzfv jdk-8u181-linux-x64.tar.gz
~~~

#### Renomear a pasta do **Java JDK**.
~~~
sudo mv jdk1.8.0_181/ jdk
~~~

#### Remover o **TARBALL** para manter o disco sem arquivos que não irá ser utilizados.
~~~
sudo rm -r jdk-8u181-linux-x64.tar.gz
~~~

#### Configurar as variáveis de ambiente dentro do **bash_profile**.
~~~
# Retornar a pasta raiz
cd ~

# Abrir o arquivo .bash_profile
sudo vi .bash_profile

## Incluir o conteudo abaixo no final do arquivo
# Java JDK 1.8
export JAVA_HOME=/opt/jdk
export JRE_HOME=/opt/jdk/jre
export PATH=$PATH:$JAVA_HOME/bin:$JRE_HOME/bin

source .bash_profile
~~~

#### Verificar a versão do Java
~~~
java -version

## O Resultado deve ser esse abaixo:
java version "1.8.0_181"
Java(TM) SE Runtime Environment (build 1.8.0_181-b13)
Java HotSpot(TM) 64-Bit Server VM (build 25.181-b13, mixed mode)
~~~

#### Atualizar o SO
~~~
sudo yum update -y
~~~

# Configurando a Conectividade entre as Maquinas do Cluster
>**Observação:**
>
>Para configurar a conectividade entre as maquinas do cluster precisamos editar o arquivo hosts de ambas as máquinas do cluster incluindo o ip e o nome dns das maquinas e configurar o ssh sem senha.

## Editando o Arquivo */etc/hosts*

#### Para realizar a inclusão dos IP's e DNS edite passando o IP e o DNS no arquivo **/etc/hosts**, conforme imagem abaixo.

![](/dsa-ml-ia-ambientes-distribuidos/02_configurando_multinode_spark/imgs/etapa-7-config-vm.PNG)

~~~
sudo vi /etc/hosts
~~~

>**Observação:**
>
>Se você estiver configurando o Multinode Spark Cluster em máquinas EC2 desconsiderar este passo, pois segundo recomendações da própria AWS não podemos mexer no /etc/hosts das máquinas EC2 devido a problemas que possam ser gerados após esses ajustes.

## Criando as Chaves Públicas e Privadas para a Comunicação via SSH

#### Para realizar a criação das chaves públicas e privadas executar os comandos abaixo no nó master do cluster Spark.

~~~
# Gerando a chave com o protocolo rsa sem senha
ssh-keygen -t rsa -P ""
~~~

#### Dentro do próprio nó master é necessário copiar a chave pública para dentro do **authorized_keys**, conforme comandos abaixo.

~~~
# Acesse a pasta .ssh
cd .ssh

# Copie o conteudo do arquivo id_rsa.pub para o arquivo authorized_keys
cat id_rsa.pub >> authorized_keys
~~~

#### Antes de realizar a cópia da chave pública para os demais nós do cluster Spark, execute o comando abaixo em cada uma das máquinas do cluster.

~~~
# Crie a pasta .ssh
mkdir .ssh
~~~

#### Para realizar a cópia da chave pública para dentro dos demais nós do cluster Spark, execute os comandos abaixos no nós master.

~~~
# Execute o comando abaixo para copiar o arquivo authorized_keys para o node1
scp authorized_keys aluno@node1:/home/aluno/.ssh

# Execute o comando abaixo para copiar o arquivo authorized_keys para o node2
scp authorized_keys aluno@node2:/home/aluno/.ssh
~~~

>**Observação:**
>
> Os nomes dados para as vm's (master, node1 e node2) podem ser substituídos pelos nomes que você escolher.

#### Dentro dos nodes escravos do cluster Spark, execute os comandos abaixo para validar que o arquivo **authorized_keys** esteja dentro da pasta **.ssh**.

~~~
# Acesse a pasta .ssh
cd .ssh

# Imprima o conteúdo do arquivo authorized_keys
cat authorized_keys
~~~

#### A saída do console deve ser algo parecido com a imagem abaixo

![](/dsa-ml-ia-ambientes-distribuidos/02_configurando_multinode_spark/imgs/etapa-8-config-vm.PNG)

#### Testar a conectividade do NodeMaster com os NodeSlave
~~~
# Testar a conectividade com o sparkslave1
ssh node1

# Testar a conectividade com o sparkslave2
ssh node2
~~~

>**Observação:**
>
> Caso no teste de conectividade acima solicitar a senha verifique os previlégios dos arquivos authorized_keys e da pasta .ssh

# Instalando o Apache Spark
>**Observação:**
>
> Realize os passos abaixo em todos os nós do cluster Spark.


#### Acesse a pasta */opt* antes de realizar os passos seguintes.
~~~
cd /opt
~~~

#### Faça o download da versão mais recente do Apache Spark.
~~~
sudo wget https://dlcdn.apache.org/spark/spark-3.2.1/spark-3.2.1-bin-hadoop3.2.tgz
~~~

#### Descompacte o **TARBAL** do Apache Spark
~~~
sudo tar xvfz spark-3.2.1-bin-hadoop3.2.tgz
~~~

#### Remova o **TARBALL** do Apache Spark para manter a memória de armazenamento sem lixo.
~~~
sudo rm spark-3.2.1-bin-hadoop3.2.tgz
~~~

#### Renomeie o **spark-...-bin-hadoop...tgz** para spark.
~~~
sudo mv spark-3.2.1-bin-hadoop3.2/ spark
~~~

#### Incluir o **bin** do spark nas variáveis de ambiente.
~~~
# Retornar a pasta raiz
cd ~

# Abrir o arquivo .bash_profile
sudo vi .bash_profile

## Incluir os seguintes parâmetros abaixo no final do arquivo e salve-o
# Spark 3.2.1
export SPARK_HOME=/opt/spark
export PATH=$PATH:$SPARK_HOME/bin

# Executo o comando source para que a variável de ambiente seja inicializada
source .bash_profile
~~~

#### Teste se o Apache Spark está funcionando, com o comando abaixo.
~~~
spark-shell
~~~

# Configurando o Cluster Apache Spark
> **Observação:**
>
> 1. As configurações abaixo são as configurações iniciais para inicializar o cluster Spark e dar início nas atividades referentes ao uso do **Multinode Cluster Spark**. Configurações referentes ao pyspark serão abordadas em outros capítulos do curso.
> 2. 

#### Acesse a pasta **/opt/spark/conf** antes de começar a realizar as configurações.
~~~
cd /opt/spark/conf
~~~

#### Criar uma cópia dos arquivos **spark-env.sh.template** e **workers.template**.
~~~
# Copiar o arquivo spark-env.sh
cp spark-env.sh.template spark-env.sh

# Copiar o arquivo workers.template workers
cp workers.template workers
~~~

#### Configurar os parâmetros do arquivo **workers** em todas as máquinas do cluster, passando os dns node1 e node2 e excluindo o localhost.
~~~
vi workers
~~~

#### O arquivo deverá ficar parecido com a imagem abaixo.
![](/dsa-ml-ia-ambientes-distribuidos/02_configurando_multinode_spark/imgs/etapa-9-config-vm.PNG)

#### Configurar os parâmetros **SPARK_MASTER_HOST** e **JAVA_HOME** do arquivo **spark-env.sh** em todas as máquinas do cluster, conforme abaixo.
~~~
# Abrir o arquivo spark-env.sh
vi spark-env.sh

# Configurar o parâmetro SPARK_MASTER_HOST passando o ip do nó master, conforme abaixo.
export SPARK_MASTER_HOST=192.168.15.134

# Configurar o parâmetro JAVA_HOME passando o caminho do JAVA JDK, conforme abaixo.
export JAVA_HOME=/opt/jdk
~~~

#### O arquivo deverá ficar parecido com a imagem abaixo.
![](/dsa-ml-ia-ambientes-distribuidos/02_configurando_multinode_spark/imgs/etapa-10-config-vm.PNG)

#### Inicializar o cluster Spark.
~~~
./sbin/start-all.sh
~~~

#### Verificar se o cluster Spark está em funcionamento, executando o comando abaixo em todos os nós
~~~
jps
~~~

#### A saída do comando será algo parecido com a imagem abaixo.
![](/dsa-ml-ia-ambientes-distribuidos/02_configurando_multinode_spark/imgs/etapa-11-config-vm.PNG)