"""Synthetic button-state exercise. No process access, injection or keyboard API."""
MIRROR=(4,3,2,1,0,7,6,5,8)

def render_buttons(previous_down,desired_down):
    if len(previous_down)!=4 or len(desired_down)!=4 or any(type(v) is not bool for v in (*previous_down,*desired_down)):
        raise ValueError('Require four boolean physical states')
    return [3 if before and now else 0 if now else 1 if before else 4 for before,now in zip(previous_down,desired_down)]

def mirror_direction(direction):
    if type(direction) is not int or not 0<=direction<=8:raise ValueError('Unknown direction')
    return MIRROR[direction]

if __name__=='__main__':
    previous=[False]*4
    for desired in ([True,False,False,False],[True,False,False,False],[False]*4):
        print(render_buttons(previous,desired));previous=list(desired)
