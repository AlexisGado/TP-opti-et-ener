\* data/question8.lp *\
Minimize
OBJ: 20 prod_0_thf1 + 44 prod_0_thf2 + 100 prod_0_thf3 + 20 prod_1_thf1
 + 44 prod_1_thf2 + 100 prod_1_thf3 + 20 prod_2_thf1 + 44 prod_2_thf2
 + 100 prod_2_thf3 + 20 prod_3_thf1 + 44 prod_3_thf2 + 100 prod_3_thf3
Subject To
balance_0: prod_0_hyd_00 + prod_0_thf1 + prod_0_thf2 + prod_0_thf3 = 1000
balance_1: prod_1_hyd_00 + prod_1_thf1 + prod_1_thf2 + prod_1_thf3 = 1600
balance_2: prod_2_hyd_00 + prod_2_thf1 + prod_2_thf2 + prod_2_thf3 = 600
balance_3: prod_3_hyd_00 + prod_3_thf1 + prod_3_thf2 + prod_3_thf3 = 900
maj_stock0: 7200 prod_0_hyd_00 + reservoir_0_0 = 1440000
maj_stock1: 7200 prod_1_hyd_00 - reservoir_0_0 + reservoir_1_0 = 0
maj_stock2: 7200 prod_2_hyd_00 - reservoir_1_0 + reservoir_2_0 = 0
maj_stock3: 7200 prod_3_hyd_00 - reservoir_2_0 + reservoir_3_0 = 0
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
maximum_stock0_0: reservoir_0_0 <= 1440000
maximum_stock1_0: reservoir_1_0 <= 1440000
maximum_stock2_0: reservoir_2_0 <= 1440000
maximum_stock3_0: reservoir_3_0 <= 1440000
minimum_production0_thf1: prod_0_thf1 >= 0
minimum_production0_thf2: prod_0_thf2 >= 0
minimum_production0_thf3: prod_0_thf3 >= 0
minimum_production1_thf1: prod_1_thf1 >= 0
minimum_production1_thf2: prod_1_thf2 >= 0
minimum_production1_thf3: prod_1_thf3 >= 0
minimum_production2_thf1: prod_2_thf1 >= 0
minimum_production2_thf2: prod_2_thf2 >= 0
minimum_production2_thf3: prod_2_thf3 >= 0
minimum_production3_thf1: prod_3_thf1 >= 0
minimum_production3_thf2: prod_3_thf2 >= 0
minimum_production3_thf3: prod_3_thf3 >= 0
minimum_stock0_0: reservoir_0_0 >= 0
minimum_stock1_0: reservoir_1_0 >= 0
minimum_stock2_0: reservoir_2_0 >= 0
minimum_stock3_0: reservoir_3_0 >= 0
shutdown_t_2_thf1: status_2_thf1 = 0
Bounds
prod_0_hyd_00 <= 75
prod_0_thf1 <= 1000
prod_0_thf2 <= 550
prod_0_thf3 <= 200
prod_1_hyd_00 <= 75
prod_1_thf1 <= 1000
prod_1_thf2 <= 550
prod_1_thf3 <= 200
prod_2_hyd_00 <= 75
prod_2_thf1 = 0
prod_2_thf2 <= 550
prod_2_thf3 <= 200
prod_3_hyd_00 <= 75
prod_3_thf1 <= 1000
prod_3_thf2 <= 550
prod_3_thf3 <= 200
reservoir_0_0 free
reservoir_1_0 free
reservoir_2_0 free
reservoir_3_0 free
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
End
