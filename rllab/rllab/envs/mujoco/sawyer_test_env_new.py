import numpy as np

from rllab.core.serializable import Serializable
from rllab.envs.base import Step
from rllab.envs.mujoco.mujoco_env import MujocoEnv
from rllab.misc import autoargs
from rllab.misc.overrides import overrides


# based on inverted_double_pendulum_env.py

class SawyerTestEnv(MujocoEnv, Serializable):

    FILE = 'sawyer_gripper_mocap.xml'

    def __init__(
            self, action_mode='torque',
            *args, **kwargs):
        self.goal_pos = np.array([0.65663183,  0.16704036,  -0.11950524]) 
        super(SawyerTestEnv, self).__init__(*args, **kwargs)
        Serializable.quick_init(self, locals())
        self.goal_pos = self.data.xpos[self.model.body_names.index('target')].copy()
        print('Target ID = ', self.model.body_names.index('target'))
        print('Target posit,ion: ', self.goal_pos)
        print('Starting position:', self.get_endeff_pos())
        self.kill_radius = 0.5
        self.kill_outside = True # experimental feature, produces errors
    @overrides
    def get_current_obs(self):
        return np.concatenate([
            self.model.data.qpos.flat[0:7],  # [0:7] to delete the gripper measurements. The gripper is not used when holding the gear
            self.model.data.qvel.flat[0:7],
            self.get_vec_to_goal()           # added the vector to the goal  to test if it improves the learning
            #self.goal_pos, # goal position
        ])
    #alternative:
    '''
    @overrides
    def get_current_obs(self):
        return self.get_body_com('right_hand')
    '''

    @overrides
    def step(self, action):
        self.forward_dynamics(action)
        next_obs = self.get_current_obs()
        #print(next_obs)
        distance_to_goal = self.get_distance_to_goal()
        #reward = -distance_to_goal
        # modified reward with more emphesis on the xy-position
        vec = self.get_vec_to_goal()
        reward = - np.linalg.norm(vec, ord=1)
        #print('reward = ', reward)
        done = False 
        if reward > -0.03:
            done = True 
            reward = reward + 100
            print("******** Reached Target ********")
        if self.kill_outside and (distance_to_goal > self.kill_radius):
            done = True
            reward = reward - 100
            print("******** OUT of region ********")
        return Step(next_obs, reward, done)
        

    @property
    def endeff_id(self):
        #print('goal_id = ',self.model.body_names.index('goal'))
        return self.model.body_names.index('r_gripper_tool_frame') 

    def get_endeff_pos(self):
        return self.data.xpos[self.endeff_id].copy()

    def get_goal_position(self):
        return self.goal_pos

    def get_vec_to_goal(self):
        endeff_pos = self.get_endeff_pos()
        goal_pos = self.get_goal_position()
        return endeff_pos - goal_pos 

    def get_distance_to_goal(self):
        vec_to_goal = self.get_vec_to_goal()
        return np.linalg.norm(vec_to_goal)
    """
    def set_state(self, qpos, qvel):
        #assert qpos.shape == (self.model.nq, 1) and qvel.shape == (self.model.nv, 1)
        self.model.data.qpos = qpos
        self.model.data.qvel = qvel
        # self.model._compute_subtree() #pylint: disable=W0212
        self.model.forward()
    """