# Git

开梯子后拉github的项目一直拉不下来，一看是所有的请求都走了梯子的代理，需要手动配置git config --global http.proxy http://127.0.0.1:7890，让git的请求也走代理。

如果后面不想让请求都走代理，那么可以git config --global --unset http.proxy移除掉。