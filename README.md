# SawyerSQL

#Installing Soft Q-Learning with Sawyer Model: Time for installation: ~ 1 hour
Instructions written by Gerrit Schoettler, 04/12/2018 (gerrit.schoettler@berkeley.edu)
Updated 14/05/2018

1. Install Ubuntu 16.04.4 LTS or 18.04 LTS
http://releases.ubuntu.com/16.04/. Install the 64-bit PC (AMD) Version of
Ubuntu 16.04 LTS Desktop, even if you have an Intel CPU. The complete installation has also
Been performed successfully on Ubuntu 18.04 LTS 64-bit PC (AMD64): 
http://releases.ubuntu.com/18.04/
It is fine to install Ubuntu as a virtual machine in VMware Workstation Player 14. 
30 GB of hard drive memory are recommended. 

2. Update all:
sudo apt-get update
sudo apt-get upgrade
sudo apt-get dist-upgrade

3. Get a Mujoco License from https://www.roboti.us/license.html . Download the Computer-id file for Linux, then:
cd Downloads
chmod +x getit_linux 
./getid_linux
4. Install git (sudo apt install git) and pip (sudo apt install python-pip) and miniconda (Python 3.6, 64-bit https://conda.io/docs/user-guide/install/linux.html). Close terminal after installing miniconda.  

5. Install Sublime
http://tipsonubuntu.com/2017/05/30/install-sublime-text-3-ubuntu-16-04-official-way/
sudo apt-get update
sudo apt-get install sublime-text

6. Start installation of Soft Q-Learning 
https://github.com/haarnoja/softqlearning 
Choose local installation, follow instructions, starting with cloning rllab. 
Choose “<installation_path_of_your_choice>” = “~/projectThesis”.
After creating conda environment:   % ignore numpy update message 
Test example experiments: 
 cd ~/projectThesis/rllab
export PYTHONPATH=$(pwd):${PYTHONPATH}
cd ..
cd softqlearning
source activate sql

Run swimmer example for 1 minute to test installation (edit log_dir):
python ./examples/mujoco_all_sql.py --env=swimmer --log_dir="/home/gerrit/projectThesis/data/swimmer-experiment"
Execute this command twice if the reinforcement learning does not start at the first time. 

To visualize swimmer example (edit log_dir): 
python ./scripts/sim_policy.py --max-path-length 1000 --speedup 100 /home/gerrit/projectThesis/data/swimmer-experiment/params.pkl

7. Implemenation of Sawyer model: 
Download and save all files from rllab/vendor/mujoco_models. These files are named “mesh”, “sawyer_gripper_mocap.xml” and “sawyer_gripper_mocap_unedited.xml”. 
Copy “mesh” and “sawyer_gripper_mocap.xml” to /home/gerrit/projectThesis/rllab/vendor/mujoco_models
(edit path if project path is not /home/gerrit/projectThesis/)

8. Include Sawyer environment:
Download and save the file from rllab/rllab/envs/mujoco. This file is named “sawyer_test_env_new.py”. 
Copy the file  to  ~/gerrit/projectThesis/rllab/rllab/envs/mujoco
Download and save all files from softqlearning/examples. These files are named “mujoco_all_sql.py” and “reuse_qf_policy_sawyer.py”. 
Copy both files to ~/gerrit/projectThesis/softqlearning/examples  and replace the old version of it. Just the SawyerTestEnv got added, no other changes were made. 
(edit path if project path is not /home/gerrit/projectThesis/)

9. Run Sawyer experiment:
cd ~/projectThesis/rllab
export PYTHONPATH=$(pwd):${PYTHONPATH}
cd ..
cd softqlearning
source activate sql
python ./examples/mujoco_all_sql.py --env=sawyer --log_dir="/home/gerrit/projectThesis/data/sawyer-experiment"
(Keep running for some iterations)

Visualize Sawyer:
python ./scripts/sim_policy.py --max-path-length 1000 --speedup 100 /home/gerrit/projectThesis/data/sawyer-experiment/itr_0.pkl

(edit path if project path is not /home/gerrit/projectThesis/)

Reuse existing policy: 

python ./examples/reuse_qf_policy_sawyer.py /home/gerrit/projectThesis/data/sawyer-experiment/itr_0.pkl 

Files get saved in the data folder of softqlearning. From there we can copy them over to our saved files and rename to keep the order of iterations. This way we can keep learning after an interruption. 

To record a mp4 video:
python ./record_video.py
Video saved to /home/gerrit/projectThesis/rllab/data/video/sawyer

10. This update included:
- Big changes in the sawyer model -> Disc on peg task with a squared disc on a round peg, 
- Changes in the sawyer environment -> changes in the reward function (1-norm and rewarding correct orientation)

11. The next update will include:
- Inclusion of the SAC algorithm (https://github.com/haarnoja/sac) -> this was difficult to install because it required changes in the environment.yml file (of SAC) before building the conda environment. 
Contact Gerrit Schoettler for previews this update. 
