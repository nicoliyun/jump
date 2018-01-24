#!groovy
pipeline {
    //在任何可用的代理上执行Pipeline
    agent any
    //参数化变量，目前只支持[booleanParam, choice, credentials, file, text, password, run, string]这几种参数类型，其他高级参数化类型还需等待社区支持。
    parameters {
    //git代码路径【参数值对外隐藏】
    string(name:'repoUrl', defaultValue: 'git@192.168.20.10:core/core-server.git', description: 'git代码路径')
    //repoBranch参数后续替换成git parameter不再依赖手工输入,JENKINS-46451【git parameters目前还不支持pipeline】
    string(name:'repoBranch', defaultValue: 'master', description: 'git分支名称')
    //编译目录的相对路径
    string(name:'buildPath', defaultValue: 'core-service', description: '编译目录')
    //jar包的相对路径
    string(name:'jarLocation', defaultValue: 'core-service/build/libs/core-service-1.0.0-SNAPSHOT.jar', description: 'jar包的相对路径')
    //服务器参数采用了组合方式，避免多次选择
    choice(name: 'server',choices:'192.168.20.144,\n192.168.20.111,\n192.168.20.145', description: '测试服务器列表选择(IP)')
     //重启脚本的绝对路径
    string(name:'shellpath', defaultValue: '/Data/apps/core-service', description: '重启脚本的绝对路径')
    }
    //常量参数，初始确定后一般不需更改
    environment{
        //git服务全系统只读账号cred_id【参数值对外隐藏】
        CRED_ID='77f987d0-7559-4343-bab8-bd8d9938b628'
    }
    options {
        //保持构建的最大个数
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    //pipeline的各个阶段场景
    stages {
        stage('清理工作空间') {
            steps {
                cleanWs()
                  }
        }

        stage('代码获取') {
            steps {
            //根据param.server分割获取参数,包括IP,jettyPort,username,password
            script {
                def split=params.server.split(",")
                serverIP=split[0]
            }
              echo "starting fetchCode from ${params.repoUrl},${params.repoBranch}......"
              // Get some code from a GitHub repository
              git credentialsId:CRED_ID, url:params.repoUrl, branch:params.repoBranch
            }
        }

        stage('编译') {
            steps {
              //根据编译路径打包
              echo "starting build in ${workspace}/${params.buildPath} ......"
              // Get some code from a GitHub repository
              sh "cd ${params.buildPath} && gradle bootRepackage"
            }
        }

        stage('推送测试包'){
            steps {
             echo "starting deploy to ${serverIP}......"
             //发布jar包到指定服务器
             sh "scp ${params.jarLocation} root@${serverIP}:${params.shellpath}"
            }
        }
        stage('重启应用'){
            steps {
             echo "restart restart app......"
             //发布jar包到指定服务器
             sh "ssh root@${serverIP} sh ${params.shellpath}/restart.sh"
            }
        }
    }
}