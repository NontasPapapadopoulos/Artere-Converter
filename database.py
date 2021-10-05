import pandapower as pp 
from pandapower.control.controller.trafo.ContinuousTapControl import ContinuousTapControl

net = pp.create_empty_network(f_hz=50.0, sn_mva=100)
    
    
# list of Buses:
EQGEN = pp.create_bus(net, vn_kv=220.0, name="EQGEN", in_service=True)
N4 = pp.create_bus(net, vn_kv=20.0, name="N4", in_service=True)
N10 = pp.create_bus(net, vn_kv=20.0, name="N10", in_service=True)
N25 = pp.create_bus(net, vn_kv=20.0, name="N25", in_service=True)
N5 = pp.create_bus(net, vn_kv=20.0, name="N5", in_service=True)
N7 = pp.create_bus(net, vn_kv=20.0, name="N7", in_service=True)
N8 = pp.create_bus(net, vn_kv=20.0, name="N8", in_service=True)
N11 = pp.create_bus(net, vn_kv=20.0, name="N11", in_service=True)
N13 = pp.create_bus(net, vn_kv=20.0, name="N13", in_service=True)
N14 = pp.create_bus(net, vn_kv=20.0, name="N14", in_service=True)
N17 = pp.create_bus(net, vn_kv=20.0, name="N17", in_service=True)
N19 = pp.create_bus(net, vn_kv=20.0, name="N19", in_service=True)
N20 = pp.create_bus(net, vn_kv=20.0, name="N20", in_service=True)
N23 = pp.create_bus(net, vn_kv=20.0, name="N23", in_service=True)
N24 = pp.create_bus(net, vn_kv=20.0, name="N24", in_service=True)
N26 = pp.create_bus(net, vn_kv=20.0, name="N26", in_service=True)
N28 = pp.create_bus(net, vn_kv=20.0, name="N28", in_service=True)
N29 = pp.create_bus(net, vn_kv=20.0, name="N29", in_service=True)
N3 = pp.create_bus(net, vn_kv=20.0, name="N3", in_service=True)
N1 = pp.create_bus(net, vn_kv=20.0, name="N1", in_service=True)
N2 = pp.create_bus(net, vn_kv=20.0, name="N2", in_service=True)
N30 = pp.create_bus(net, vn_kv=20.0, name="N30", in_service=True)
N6 = pp.create_bus(net, vn_kv=20.0, name="N6", in_service=True)
N9 = pp.create_bus(net, vn_kv=20.0, name="N9", in_service=True)
N12 = pp.create_bus(net, vn_kv=20.0, name="N12", in_service=True)
N15 = pp.create_bus(net, vn_kv=20.0, name="N15", in_service=True)
N18 = pp.create_bus(net, vn_kv=20.0, name="N18", in_service=True)
N22 = pp.create_bus(net, vn_kv=20.0, name="N22", in_service=True)
N21 = pp.create_bus(net, vn_kv=20.0, name="N21", in_service=True)
N27 = pp.create_bus(net, vn_kv=20.0, name="N27", in_service=True)
N16 = pp.create_bus(net, vn_kv=20.0, name="N16", in_service=True)


# list of Loads:
pp.create_load(net, bus=N4, p_mw=-4.5, q_mvar=-1.5, name="N4", in_service=True)
pp.create_load(net, bus=N10, p_mw=-4.5, q_mvar=-2.0, name="N10", in_service=True)
pp.create_load(net, bus=N25, p_mw=-4.5, q_mvar=-2.0, name="N25", in_service=True)
pp.create_load(net, bus=N5, p_mw=0.7, q_mvar=0.21, name="N5", in_service=True)
pp.create_load(net, bus=N7, p_mw=0.22, q_mvar=0.09, name="N7", in_service=True)
pp.create_load(net, bus=N8, p_mw=0.33, q_mvar=0.11, name="N8", in_service=True)
pp.create_load(net, bus=N11, p_mw=0.9, q_mvar=0.45, name="N11", in_service=True)
pp.create_load(net, bus=N13, p_mw=0.35, q_mvar=0.15, name="N13", in_service=True)
pp.create_load(net, bus=N14, p_mw=1.26, q_mvar=0.64, name="N14", in_service=True)
pp.create_load(net, bus=N17, p_mw=0.76, q_mvar=0.43, name="N17", in_service=True)
pp.create_load(net, bus=N19, p_mw=1.22, q_mvar=0.46, name="N19", in_service=True)
pp.create_load(net, bus=N20, p_mw=0.95, q_mvar=0.43, name="N20", in_service=True)
pp.create_load(net, bus=N23, p_mw=0.4, q_mvar=0.17, name="N23", in_service=True)
pp.create_load(net, bus=N24, p_mw=0.44, q_mvar=0.205, name="N24", in_service=True)
pp.create_load(net, bus=N26, p_mw=0.9, q_mvar=0.45, name="N26", in_service=True)
pp.create_load(net, bus=N28, p_mw=1.05, q_mvar=0.625, name="N28", in_service=True)
pp.create_load(net, bus=N29, p_mw=0.68, q_mvar=0.31, name="N29", in_service=True)
pp.create_load(net, bus=N3, p_mw=0.85, q_mvar=0.52, name="N3", in_service=True)
pp.create_load(net, bus=N16, p_mw=-3.0, q_mvar=0.0, name="N16", in_service=True)


# List of Shunts:


# list of Lines:
pp.create_line_from_parameters(net, from_bus=N30, to_bus=N1, name="N30-N1", length_km=1, r_ohm_per_km=0.1464, x_ohm_per_km=0.4116, max_i_ka=288.646267, c_nf_per_km=0.000000, in_service=True)
pp.create_line_from_parameters(net, from_bus=N1, to_bus=N2, name="N1-N2", length_km=1, r_ohm_per_km=0.122, x_ohm_per_km=0.343, max_i_ka=288.646267, c_nf_per_km=0.000000, in_service=True)
pp.create_line_from_parameters(net, from_bus=N2, to_bus=N3, name="N2-N3", length_km=1, r_ohm_per_km=0.1342, x_ohm_per_km=0.3773, max_i_ka=288.646267, c_nf_per_km=0.000000, in_service=True)
pp.create_line_from_parameters(net, from_bus=N2, to_bus=N4, name="N2-N4", length_km=1, r_ohm_per_km=0.1708, x_ohm_per_km=0.4802, max_i_ka=288.646267, c_nf_per_km=0.000000, in_service=True)
pp.create_line_from_parameters(net, from_bus=N4, to_bus=N5, name="N4-N5", length_km=1, r_ohm_per_km=0.122, x_ohm_per_km=0.343, max_i_ka=288.646267, c_nf_per_km=0.000000, in_service=True)
pp.create_line_from_parameters(net, from_bus=N4, to_bus=N6, name="N4-N6", length_km=1, r_ohm_per_km=0.122, x_ohm_per_km=0.343, max_i_ka=288.646267, c_nf_per_km=0.000000, in_service=True)
pp.create_line_from_parameters(net, from_bus=N6, to_bus=N7, name="N6-N7", length_km=1, r_ohm_per_km=0.1342, x_ohm_per_km=0.3773, max_i_ka=288.646267, c_nf_per_km=0.000000, in_service=True)
pp.create_line_from_parameters(net, from_bus=N7, to_bus=N8, name="N7-N8", length_km=1, r_ohm_per_km=0.1464, x_ohm_per_km=0.4116, max_i_ka=288.646267, c_nf_per_km=0.000000, in_service=True)
pp.create_line_from_parameters(net, from_bus=N1, to_bus=N9, name="N1-N9", length_km=1, r_ohm_per_km=0.1464, x_ohm_per_km=0.4116, max_i_ka=288.646267, c_nf_per_km=0.000000, in_service=True)
pp.create_line_from_parameters(net, from_bus=N9, to_bus=N10, name="N9-N10", length_km=1, r_ohm_per_km=0.1464, x_ohm_per_km=0.4116, max_i_ka=288.646267, c_nf_per_km=0.000000, in_service=True)
pp.create_line_from_parameters(net, from_bus=N15, to_bus=N16, name="N15-N16", length_km=1, r_ohm_per_km=0.1342, x_ohm_per_km=0.3773, max_i_ka=288.646267, c_nf_per_km=0.000000, in_service=True)
pp.create_line_from_parameters(net, from_bus=N16, to_bus=N17, name="N16-N17", length_km=1, r_ohm_per_km=0.122, x_ohm_per_km=0.343, max_i_ka=288.646267, c_nf_per_km=0.000000, in_service=True)
pp.create_line_from_parameters(net, from_bus=N16, to_bus=N18, name="N16-N18", length_km=1, r_ohm_per_km=0.1586, x_ohm_per_km=0.4459, max_i_ka=288.646267, c_nf_per_km=0.000000, in_service=True)
pp.create_line_from_parameters(net, from_bus=N18, to_bus=N19, name="N18-N19", length_km=1, r_ohm_per_km=0.1342, x_ohm_per_km=0.3773, max_i_ka=288.646267, c_nf_per_km=0.000000, in_service=True)
pp.create_line_from_parameters(net, from_bus=N19, to_bus=N20, name="N19-N20", length_km=1, r_ohm_per_km=0.122, x_ohm_per_km=0.343, max_i_ka=288.646267, c_nf_per_km=0.000000, in_service=True)
pp.create_line_from_parameters(net, from_bus=N15, to_bus=N21, name="N15-N21", length_km=1, r_ohm_per_km=0.1464, x_ohm_per_km=0.4116, max_i_ka=288.646267, c_nf_per_km=0.000000, in_service=True)
pp.create_line_from_parameters(net, from_bus=N21, to_bus=N22, name="N21-N22", length_km=1, r_ohm_per_km=0.1464, x_ohm_per_km=0.4116, max_i_ka=288.646267, c_nf_per_km=0.000000, in_service=True)
pp.create_line_from_parameters(net, from_bus=N22, to_bus=N23, name="N22-N23", length_km=1, r_ohm_per_km=0.1342, x_ohm_per_km=0.3773, max_i_ka=288.646267, c_nf_per_km=0.000000, in_service=True)
pp.create_line_from_parameters(net, from_bus=N22, to_bus=N24, name="N22-N24", length_km=1, r_ohm_per_km=0.122, x_ohm_per_km=0.343, max_i_ka=288.646267, c_nf_per_km=0.000000, in_service=True)
pp.create_line_from_parameters(net, from_bus=N21, to_bus=N25, name="N21-N25", length_km=1, r_ohm_per_km=0.1586, x_ohm_per_km=0.4459, max_i_ka=288.646267, c_nf_per_km=0.000000, in_service=True)
pp.create_line_from_parameters(net, from_bus=N10, to_bus=N11, name="N10-N11", length_km=1, r_ohm_per_km=0.122, x_ohm_per_km=0.343, max_i_ka=288.646267, c_nf_per_km=0.000000, in_service=True)
pp.create_line_from_parameters(net, from_bus=N10, to_bus=N12, name="N10-N12", length_km=1, r_ohm_per_km=0.122, x_ohm_per_km=0.343, max_i_ka=288.646267, c_nf_per_km=0.000000, in_service=True)
pp.create_line_from_parameters(net, from_bus=N12, to_bus=N13, name="N12-N13", length_km=1, r_ohm_per_km=0.122, x_ohm_per_km=0.343, max_i_ka=288.646267, c_nf_per_km=0.000000, in_service=True)
pp.create_line_from_parameters(net, from_bus=N13, to_bus=N14, name="N13-N14", length_km=1, r_ohm_per_km=0.122, x_ohm_per_km=0.343, max_i_ka=288.646267, c_nf_per_km=0.000000, in_service=True)
pp.create_line_from_parameters(net, from_bus=N9, to_bus=N15, name="N9-N15", length_km=1, r_ohm_per_km=0.1342, x_ohm_per_km=0.3773, max_i_ka=288.646267, c_nf_per_km=0.000000, in_service=True)
pp.create_line_from_parameters(net, from_bus=N25, to_bus=N26, name="N25-N26", length_km=1, r_ohm_per_km=0.1464, x_ohm_per_km=0.4116, max_i_ka=288.646267, c_nf_per_km=0.000000, in_service=True)
pp.create_line_from_parameters(net, from_bus=N25, to_bus=N27, name="N25-N27", length_km=1, r_ohm_per_km=0.1464, x_ohm_per_km=0.4116, max_i_ka=288.646267, c_nf_per_km=0.000000, in_service=True)
pp.create_line_from_parameters(net, from_bus=N27, to_bus=N28, name="N27-N28", length_km=1, r_ohm_per_km=0.1586, x_ohm_per_km=0.4459, max_i_ka=288.646267, c_nf_per_km=0.000000, in_service=True)
pp.create_line_from_parameters(net, from_bus=N27, to_bus=N29, name="N27-N29", length_km=1, r_ohm_per_km=0.1342, x_ohm_per_km=0.3773, max_i_ka=288.646267, c_nf_per_km=0.000000, in_service=True)


# list of Transformers:
pp.create_transformer_from_parameters(net, hv_bus=EQGEN, lv_bus=N30, sn_mva=20.0, name="MAINTR", shift_degree=0.0, vn_hv_kv=220.0, vn_lv_kv=20.0, vkr_percent=0.0, vk_percent=15.0, pfe_kw=0, i0_percent=0.0, in_service=True)


# list of Generators:
pp.create_gen(net, p_mw=0.0, max_q_mvar=999.0, min_q_mvar=-999.0, sn_mva=0, bus=EQGEN, vm_pu=1.002, name="EQGEN", slack=True, in_service=True)


# List of Switches:


# List of controllers:

init_va_degree_list = [] 
init_vm_pu_list = []
    
    
# Run power flow
if len(init_va_degree_list) > 0 and len(init_vm_pu_list) > 0:
    pp.runpp(net, init_va_degree=init_va_degree_list, init_vm_pu=init_vm_pu_list)
else:
    pp.runpp(net)
    
    
print(net.res_bus)          # bus results
