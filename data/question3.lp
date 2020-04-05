\* data/question3.lp *\
Minimize
OBJ: 20 prod_0_thf1 + 44 prod_0_thf2 + 100 prod_0_thf3 + 20 prod_1_thf1
 + 44 prod_1_thf2 + 100 prod_1_thf3 + 20 prod_2_thf1 + 44 prod_2_thf2
 + 100 prod_2_thf3 + 20 prod_3_thf1 + 44 prod_3_thf2 + 100 prod_3_thf3
Subject To
and_1_0_thf1: - status_0_thf1 + switch_0_thf1 = 0
and_1_0_thf2: - status_0_thf2 + switch_0_thf2 = 0
and_1_0_thf3: - status_0_thf3 + switch_0_thf3 = 0
and_2_1_thf1: status_0_thf1 - status_1_thf1 + switch_1_thf1 >= 0
and_2_1_thf2: status_0_thf2 - status_1_thf2 + switch_1_thf2 >= 0
and_2_1_thf3: status_0_thf3 - status_1_thf3 + switch_1_thf3 >= 0
and_2_2_thf1: status_1_thf1 - status_2_thf1 + switch_2_thf1 >= 0
and_2_2_thf2: status_1_thf2 - status_2_thf2 + switch_2_thf2 >= 0
and_2_2_thf3: status_1_thf3 - status_2_thf3 + switch_2_thf3 >= 0
and_2_3_thf1: status_2_thf1 - status_3_thf1 + switch_3_thf1 >= 0
and_2_3_thf2: status_2_thf2 - status_3_thf2 + switch_3_thf2 >= 0
and_2_3_thf3: status_2_thf3 - status_3_thf3 + switch_3_thf3 >= 0
and_3_1_thf1: status_0_thf1 + switch_1_thf1 <= 1
and_3_1_thf2: status_0_thf2 + switch_1_thf2 <= 1
and_3_1_thf3: status_0_thf3 + switch_1_thf3 <= 1
and_3_2_thf1: status_1_thf1 + switch_2_thf1 <= 1
and_3_2_thf2: status_1_thf2 + switch_2_thf2 <= 1
and_3_2_thf3: status_1_thf3 + switch_2_thf3 <= 1
and_3_3_thf1: status_2_thf1 + switch_3_thf1 <= 1
and_3_3_thf2: status_2_thf2 + switch_3_thf2 <= 1
and_3_3_thf3: status_2_thf3 + switch_3_thf3 <= 1
and_4_1_thf1: - status_1_thf1 + switch_1_thf1 <= 0
and_4_1_thf2: - status_1_thf2 + switch_1_thf2 <= 0
and_4_1_thf3: - status_1_thf3 + switch_1_thf3 <= 0
and_4_2_thf1: - status_2_thf1 + switch_2_thf1 <= 0
and_4_2_thf2: - status_2_thf2 + switch_2_thf2 <= 0
and_4_2_thf3: - status_2_thf3 + switch_2_thf3 <= 0
and_4_3_thf1: - status_3_thf1 + switch_3_thf1 <= 0
and_4_3_thf2: - status_3_thf2 + switch_3_thf2 <= 0
and_4_3_thf3: - status_3_thf3 + switch_3_thf3 <= 0
equilibre_0: prod_0_thf1 + prod_0_thf2 + prod_0_thf3 = 1000
equilibre_1: prod_1_thf1 + prod_1_thf2 + prod_1_thf3 = 1600
equilibre_2: prod_2_thf1 + prod_2_thf2 + prod_2_thf3 = 600
equilibre_3: prod_3_thf1 + prod_3_thf2 + prod_3_thf3 = 900
maximum_production0_thf1: prod_0_thf1 - 1000 status_0_thf1 <= 0
maximum_production0_thf2: prod_0_thf2 - 550 status_0_thf2 <= 0
maximum_production0_thf3: prod_0_thf3 - 200 status_0_thf3 <= 0
maximum_production1_thf1: prod_1_thf1 - 1000 status_1_thf1 <= 0
maximum_production1_thf2: prod_1_thf2 - 550 status_1_thf2 <= 0
maximum_production1_thf3: prod_1_thf3 - 200 status_1_thf3 <= 0
maximum_production2_thf1: prod_2_thf1 <= 0
maximum_production2_thf2: prod_2_thf2 - 550 status_2_thf2 <= 0
maximum_production2_thf3: prod_2_thf3 - 200 status_2_thf3 <= 0
maximum_production3_thf1: prod_3_thf1 - 1000 status_3_thf1 <= 0
maximum_production3_thf2: prod_3_thf2 - 550 status_3_thf2 <= 0
maximum_production3_thf3: prod_3_thf3 - 200 status_3_thf3 <= 0
minimimum_production0_thf1: prod_0_thf1 >= 0
minimimum_production0_thf2: prod_0_thf2 >= 0
minimimum_production0_thf3: prod_0_thf3 - 100 status_0_thf3 >= 0
minimimum_production1_thf1: prod_1_thf1 >= 0
minimimum_production1_thf2: prod_1_thf2 >= 0
minimimum_production1_thf3: prod_1_thf3 - 100 status_1_thf3 >= 0
minimimum_production2_thf1: prod_2_thf1 >= 0
minimimum_production2_thf2: prod_2_thf2 >= 0
minimimum_production2_thf3: prod_2_thf3 - 100 status_2_thf3 >= 0
minimimum_production3_thf1: prod_3_thf1 >= 0
minimimum_production3_thf2: prod_3_thf2 >= 0
minimimum_production3_thf3: prod_3_thf3 - 100 status_3_thf3 >= 0
shutdown_t_2_thf1: status_2_thf1 = 0
Bounds
prod_0_thf1 <= 1000
prod_0_thf2 <= 550
prod_0_thf3 <= 200
prod_1_thf1 <= 1000
prod_1_thf2 <= 550
prod_1_thf3 <= 200
prod_2_thf1 = 0
prod_2_thf2 <= 550
prod_2_thf3 <= 200
prod_3_thf1 <= 1000
prod_3_thf2 <= 550
prod_3_thf3 <= 200
Binaries
status_0_thf1
status_0_thf2
status_0_thf3
status_1_thf1
status_1_thf2
status_1_thf3
status_2_thf1
status_2_thf2
status_2_thf3
status_3_thf1
status_3_thf2
status_3_thf3
switch_0_thf1
switch_0_thf2
switch_0_thf3
switch_1_thf1
switch_1_thf2
switch_1_thf3
switch_2_thf1
switch_2_thf2
switch_2_thf3
switch_3_thf1
switch_3_thf2
switch_3_thf3
End
