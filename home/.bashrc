# Get the aliases and functions
if [ -f /etc/bashrc ]; then
    . /etc/bashrc
fi

# User specific environment and startup programs
function ps1() {
    export PS1="[\u@${CLUSTER_NAME} \W]\$ "
}
export PROMPT_COMMAND=ps1
export KUBECONFIG=/data/openshift-installer/auth/kubeconfig

PYTHONPATH=/app/lib/python:/deps/python
PYTHONUSERBASE=/deps/python
ANSIBLE_COLLECTIONS_PATH=/deps/ansible
PATH=/deps/python/bin:$PATH

alias ll='ls -la'
