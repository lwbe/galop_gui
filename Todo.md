# Evolution de galop.py

## supprimer la dépendance à cmd_paths ou pas

Pour supprimer l'utilisation de cmd_paths il faut retirer l'appel au méthodes suivantes:

 - Partie inititialisation du modules donc si on réécris on n'en a pas besoin. 
   - **init_space@paths**
   - **init_volume@paths**
   - **init_path@paths**
   - **deinit_space@paths**
   - **deinit_volume@paths**
   - **deinit_path@paths**
   
 - Appel au autres modules pyrame.
   - **get_position@paths**  : récupére la position courante du setup
   - **move_space@paths**    : deplace l'ensembles des platines on donne trois coordonnées et des vitesses accélération
   - **move_first@paths**    : initialise le deplacement en suivant le path 
   - **move_next@paths**     : fait la suite du path jusqu'a recevoir finished





### init_volume@paths
def init_volume_paths(volume_id,space_id,module,function,*params):
    """
    Define volume, a geometrical form with a function a set  attached to a space 
 
    -   *volume_id* the identifier of the volume 
    -   *space_id*  the space it is attache to
    -   *module*  the module containing an init_function and a function  
    -   *function* the function to define the coordinates that are inside or outside the volume 
    -   The *params* is a list of parameters needed to initialise the volume with the init_function in the module .
 
    For more information about the modules see the documentation."
    """




### init_path@paths


### get_position@paths

Cette fonction appelle get_pos@motion pour chaque axes space["motion%d_id"%(i)] 

    def init_space_paths(space_id,motion1_id,motion2_id,motion3_id,r1,r2,r3):
        "Initialize *space_id* with three id of motion system *motion_id* and three minimal step for each axis *rn*"
        r1=float(r1)
        r2=float(r2)
        r3=float(r3)
        space={"r1":r1,"r2":r2,"r3":r3,"motion1_id":motion1_id,"motion2_id":motion2_id,"motion3_id":motion3_id,"forbidden":""}
        ....


Code de la fonction.

    def get_pos(space):
        # internal function to get the position and return a list of position
        tres=[]
        for i in range(1,4):
            retcode,res=submod_execcmd("get_pos@motion",space["motion%d_id"%(i)])
            if retcode==0:
                return 0,"error getting position of axis %d <- %s"%(i,res)
            tres.append(float(res))
        return 1,tres

    def get_position_paths(space_id):
        '''
        Give the position of the motion controllers. The order is the order of the motion axis given when space was initialized.
        '''
        try:
            space=space_pool.get(space_id)
        except Exception as e:
            return 0,str(e)
        retcode,res = get_pos(space)
        return retcode,','.join(map(str,res))


### move_space@paths

Cette fonction appelle une fonction interne qui evite les zones interdites mais non prises en compte dans la version 
actuelle.

    def move(space_id,d,s,a,strategy="undef"):
        try:
            space=space_pool.get(space_id)
        except Exception as e:
            return 0,str(e)
        retcode,order=check_param(strategy,["1","2","3"],"123",int)
        if retcode==0:
            return 0,"invalid strategy: %s" % (order)

        ....

            for i in order:
                retcode,res=submod_execcmd("move@motion",space["motion%d_id"%(i)],step[i-1],s[i-1],a[i-1])
            
                if retcode==0:
                     return 0,"error moving axis %d <- %s"%(i,res)
        return 1,"ok"

    def move_space_paths(space_id,d1,d2,d3,s1,s2,s3,a1,a2,a3,strategy="undef"):
        """
        Move to a destination.

        -  *space_id* the identifier 
        -  **d**\ *i* (with *i* =1,2,3) the coordinates of the destination, 
        -  **s**\ *i* (with *i* =1,2,3) the speed, 
        -  **a**\ *i* (with *i* =1,2,3) the acceleration, 
        -  *strategy* describe the preferential order for axis movement (e.g. "213" to move first axis 2, then axis 1 finally axis 3)
        """
    
        d=[d1,d2,d3]
        s=[s1,s2,s3]
        a=[a1,a2,a3]
        retcode,res=move(space_id,d,s,a,strategy)
        if retcode==0:
            return 0,res
        return 1,"ok"


### move_first@paths

### move_next@paths
