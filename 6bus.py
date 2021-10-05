import pandapower as pp 
from pandapower.control.controller.trafo.ContinuousTapControl import ContinuousTapControl

net = pp.create_empty_network(f_hz=50, sn_mva=100)
    
    
# list of Buses:
A = pp.create_bus(net, vn_kv=15.0, name="A", in_service=True)
B = pp.create_bus(net, vn_kv=380.0, name="B", in_service=True)
C = pp.create_bus(net, vn_kv=380.0, name="C", in_service=True)
D = pp.create_bus(net, vn_kv=150.0, name="D", in_service=True)
E = pp.create_bus(net, vn_kv=150.0, name="E", in_service=True)
F = pp.create_bus(net, vn_kv=15.0, name="F", in_service=True)


# list of Loads:
pp.create_load(net, bus=D, p_mw=100.0, q_mvar=30.0, name="D", in_service=True)
pp.create_load(net, bus=E, p_mw=400.0, q_mvar=120.0, name="E", in_service=True)


# List of Shunts:


# list of Lines:
pp.create_line_from_parameters(net, from_bus=B, to_bus=C, name="B-C", length_km=1, r_ohm_per_km=1.5, x_ohm_per_km=15.0, max_i_ka=2.051113, c_nf_per_km=477.464829, in_service=True)
pp.create_line_from_parameters(net, from_bus=D, to_bus=E, name="D-E", length_km=1, r_ohm_per_km=4.0, x_ohm_per_km=20.0, max_i_ka=1.154701, c_nf_per_km=381.971863, in_service=True)


# list of Transformers:
pp.create_transformer_from_parameters(net, hv_bus=B, lv_bus=D, sn_mva=300.0, name="D-B", shift_degree=0.0, vn_hv_kv=380.0, vn_lv_kv=150.0, vkr_percent=0.0, vk_percent=14.0, pfe_kw=0, i0_percent=0.0, in_service=True)
pp.create_transformer_from_parameters(net, hv_bus=C, lv_bus=E, sn_mva=600.0, name="E-C", shift_degree=0.0, vn_hv_kv=380.0, vn_lv_kv=150.0, vkr_percent=0.0, vk_percent=14.0, pfe_kw=0, i0_percent=0.0, in_service=True)
pp.create_transformer_from_parameters(net, hv_bus=B, lv_bus=A, sn_mva=500.0, name=A-B, shift_degree=0.0, vn_hv_kv=380.0, vn_lv_kv=15.0, vkr_percent=0.0, vk_percent=14.0, pfe_kw=0, i0_percent=0.0, tap_min=8.0, tap_max=8.0, tap_step_percent=1, tap_pos=8.0,tap_neutral=0, tap_side="hv", in_service=True)
pp.create_transformer_from_parameters(net, hv_bus=B, lv_bus=F, sn_mva=250.0, name=F-B, shift_degree=0.0, vn_hv_kv=380.0, vn_lv_kv=15.0, vkr_percent=0.0, vk_percent=14.0, pfe_kw=0, i0_percent=0.0, tap_min=8.0, tap_max=8.0, tap_step_percent=1, tap_pos=8.0,tap_neutral=0, tap_side="hv", in_service=True)


# list of Generators:
pp.create_gen(net, p_mw=0.0, max_q_mvar=9999.0, min_q_mvar=-9990.0, sn_mva=500., bus=A, vm_pu=1.0, name="A", slack=True, in_service=True)
pp.create_gen(net, p_mw=150.0, max_q_mvar=9999.0, min_q_mvar=-9990.0, sn_mva=200., bus=F, vm_pu=1.0, name="F", slack=False, in_service=True)


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
