import os
import sys
if not os.getenv("DEBUG"):

    from pyrosetta import *
    from pyrosetta.teaching import *
    from pyrosetta.toolbox import cleanATOM

    pyrosetta.init()
    from pyrosetta.toolbox import pose_from_rcsb
    pose = pose_from_rcsb("1V74")
    starting_pose = pose.clone()
    cen_pose = pose.clone()
    cen_switch = SwitchResidueTypeSetMover("centroid")
    cen_switch.apply(cen_pose)
    starting_cen_pose = cen_pose.clone()

if not os.getenv("DEBUG"):
    ### BEGIN SOLUTION
    print(pose.fold_tree())
    ### END SOLUTION
if not os.getenv("DEBUG"):
    ### BEGIN SOLUTION
    print(starting_pose.fold_tree())
    print("There's 1 Jump!")
    ### END SOLUTION
if not os.getenv("DEBUG"):
    ### BEGIN SOLUITON
    from pyrosetta.rosetta.protocols.docking import setup_foldtree
    print(pose.fold_tree())
    setup_foldtree(pose, "A_B", Vector1([1]))
    setup_foldtree(starting_pose, "A_B", Vector1([1]))
    print(pose.fold_tree())
    ### END SOLUTION
    print("We changed the Jump that was connecting the N-termini of A and B into a Jump that connects the centers of A and B.")
if not os.getenv("DEBUG"):
    ### BEGIN SOLUTION
    jump_num = 1
    print(pose.jump(jump_num).get_rotation())
    print('\n')
    print(pose.jump(jump_num).get_translation())
    ### END SOLUTION
if not os.getenv("DEBUG"):
    ### BEGIN SOLUTION
    import pyrosetta.rosetta.protocols.rigid as rigid_moves
    pert_mover = rigid_moves.RigidBodyPerturbMover(jump_num, 8, 3)
    ### END SOLUTION
if not os.getenv("DEBUG"):
    from pyrosetta import PyMOLMover
    pymol = PyMOLMover()
    pymol.apply(pose)
if not os.getenv("DEBUG"):
    pert_mover.apply(pose)
    pymol.apply(pose)
if not os.getenv("DEBUG"):
    ### BEGIN SOLUTION
    randomize1 = rigid_moves.RigidBodyRandomizeMover(pose, jump_num, rigid_moves.partner_upstream)
    randomize2 = rigid_moves.RigidBodyRandomizeMover(pose, jump_num, rigid_moves.partner_downstream)
    ### END SOLUTION
if not os.getenv("DEBUG"):
    ### BEGIN SOLUTION
    randomize1.apply(pose)
    pymol.apply(pose)
    ### END SOLUTION
if not os.getenv("DEBUG"):
    ### BEGIN SOLUTION
    randomize2.apply(pose)
    pymol.apply(pose)
    ### END SOLUTION
if not os.getenv("DEBUG"):
    ### BEGIN SOLUTION
    slide = DockingSlideIntoContact(jump_num)  # for centroid mode
    slide = FaDockingSlideIntoContact(jump_num)  # for full-atom mode
    slide.apply(pose)
    pymol.apply(pose)
    ### END SOLUTION
if not os.getenv("DEBUG"):
    ### BEGIN SOLUTION
    movemap = MoveMap()
    movemap.set_jump(jump_num, True)
    min_mover = MinMover()
    min_mover.movemap(movemap)
    scorefxn = get_fa_scorefxn()
    min_mover.score_function(scorefxn)
    ### END SOLUTION
if not os.getenv("DEBUG"):
    ### BEGIN SOLUTION
    scorefxn(pose)

    min_mover.apply(pose)

    print(pose.jump(jump_num).get_rotation())
    print(pose.jump(jump_num).get_translation())
    ### END SOLUTION
if not os.getenv("DEBUG"):
    ### BEGIN SOLUTION
    scorefxn_low = create_score_function("interchain_cen")
    ### END SOLUTION
if not os.getenv("DEBUG"):
    ### BEGIN SOLUTION
    dock_lowres = DockingLowRes(scorefxn_low, jump_num)
    print(cen_pose.fold_tree())
    setup_foldtree(cen_pose, "A_B", Vector1([1]))
    print(cen_pose.fold_tree())

    dock_lowres.apply(cen_pose)
    ### END SOLUTION
if not os.getenv("DEBUG"):
    print(CA_rmsd(cen_pose, starting_cen_pose))
    print(calc_Lrmsd(cen_pose, starting_cen_pose, Vector1([1])))
if not os.getenv("DEBUG"):
    ### BEGIN SOLUTION
    jd = PyJobDistributor("output", 10, scorefxn_low)
    ### END SOLUTION
if not os.getenv("DEBUG"):
    # your starting_cen_pose should be the native crystal structure
    ### BEGIN SOLUTION
    jd.native_pose = starting_cen_pose
    ### END SOLUTION
if not os.getenv("DEBUG"):
    ### BEGIN SOLUTION
    cen_pose.assign(starting_cen_pose)

    dock_lowres.apply(cen_pose)

    jd.output_decoy(cen_pose)
    ### END SOLUTION
if not os.getenv("DEBUG"):
    ### BEGIN SOLUTION
    while not jd.job_complete:
        cen_pose.assign(starting_cen_pose)

        dock_lowres.apply(cen_pose)

        jd.output_decoy(cen_pose)
    ### END SOLUTION
if not os.getenv("DEBUG"):
    ### BEGIN SOLUTION
    jd = PyJobDistributor("output", 100, scorefxn_low)
    while not jd.job_complete:
        cen_pose.assign(starting_cen_pose)

        dock_lowres.apply(cen_pose)

        jd.output_decoy(cen_pose)
if not os.getenv("DEBUG"):
    ### BEGIN SOLUTION
    scorefxn_high = create_score_function("ref2015.wts", "docking")
    dock_hires = DockMCMProtocol()
    dock_hires.set_scorefxn(scorefxn_high)
    dock_hires.set_partners("A_B")  # make sure the FoldTree is set up properly
    ### END SOLUTION
if not os.getenv("DEBUG"):
    ### BEGIN SOLUTION
    recover_sidechains = ReturnSidechainMover(starting_pose)
    recover_sidechains.apply(pose)
    ### END SOLUTION
