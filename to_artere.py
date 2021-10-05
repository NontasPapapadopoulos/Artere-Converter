import math
from pprint import pprint
import pandas as pd

wrong_switch_type = False
line_name_list = []
trafo_name_list = []
gen_name_list = []
switch_name_list = []
sgen_name_list = []
bus_dict = {}
switch_dict = {}
line_dict = {}
gen_dict = {}
sgen_dict = {}
trafo_dict = {}
ext_grid_dict = {}
bus_names_list = []
slack_record_list = []
switch_record_list = []
bus_record_list = []
gen_record_list = []
sgen_record_list = []
ext_grid_list = []
trafo_record_list = []
line_record_list = []
line_num = 1
trafo_num = 1
gen_num = 1
sgen_num = 1
switch_num = 1


def check_status(element_status):
    if element_status == True:
        return 1
    return 0


def modify_lines(line_name):
    if line_name == "None":
        line_name = "line"
    return line_name


def modify_bus_name(bus_name):
    if type(bus_name) == int:
        bus_name = "b" + str(bus_name)
    else:
        bus_name = str(bus_name)
        if len(bus_name) > 8:
            bus_name = bus_name[:8]
        bus_name = bus_name.replace(" ", "_")
        if bus_name in bus_names_list:
            num = 2
            bus_name = list(bus_name)
            bus_name[-1] = str(num)
            bus_name = "".join(bus_name)
    return bus_name


def to_artere(net, filename):
    global frequency
    global wrong_switch_type

    # Frequency
    frequency = net.f_hz
    omega = 2 * math.pi * frequency

    # Buses
    for bus_index, bus_name, vn_kv in zip(net.bus.index, net.bus.name, net.bus.vn_kv):
        bus_dict[bus_index] = {}
        bus_dict[bus_index]['bus_name'] = modify_bus_name(bus_name)
        bus_names_list.append(modify_bus_name(bus_name))
        bus_dict[bus_index]['vn_kv'] = vn_kv

    # Loads
    for bus_index, p_mw, q_mvar, scaling in zip(net.load.bus, net.load.p_mw, net.load.q_mvar, net.load.scaling):
        bus_dict[bus_index]['Pload'] = format(p_mw, '.6f')
        bus_dict[bus_index]['Qload'] = format(q_mvar, '.6f')

    # Shunts
    try:
        for bus_index, q_mvar, p_mw in zip(net.shunt.bus, net.shunt.q_mvar, net.shunt.p_mw):
            bus_dict[bus_index]['Qshunt'] = q_mvar
            # bus_dict[bus_index]['Bshunt'] = p_mw
    except:
        pass
    pprint(bus_dict)

    df = net.line
    # Lines
    for line_index, name, from_bus, to_bus, length, Ohm_per_km, x_Ohm_per_km, capacitance_per_km, Imax, status in zip \
                (df.index, df.name, df.from_bus, df.to_bus, df.length_km, df.r_ohm_per_km, df.x_ohm_per_km,
                 df.c_nf_per_km, df.max_i_ka, df.in_service):
        line_dict[line_index] = {}
        line_dict[line_index]['name'] = name
        line_name_list.append(line_dict[line_index]['name'])
        line_dict[line_index]['from_bus'] = bus_dict[from_bus]['bus_name']
        line_dict[line_index]['to_bus'] = bus_dict[to_bus]['bus_name']
        line_dict[line_index]['Resistance'] = format(length * Ohm_per_km, '.4f')
        line_dict[line_index]['Reactance'] = format(length * x_Ohm_per_km, '.4f')
        # find half shunt susceptance
        line_capacitance = capacitance_per_km * length
        half_shunt_susceptance = (omega * line_capacitance) / 2
        half_shunt_susceptance = half_shunt_susceptance / 10 ** 3
        half_shunt_susceptance = format(half_shunt_susceptance, '.6f')
        line_dict[line_index]['half_shunt_susceptance'] = half_shunt_susceptance
        # find Snom
        voltage_bus = float(bus_dict[from_bus]['vn_kv'])
        Imax = float(Imax)
        Snom = math.sqrt(3) * Imax * float(voltage_bus)
        Snom = format(Snom, '.6f')
        line_dict[line_index]['Snom'] = Snom
        line_dict[line_index]['status'] = check_status(status)

    # Generators
    df = net.gen
    for gen_index, name, bus, p_mw, vm_pu, sn_mva, min_q_mvar, max_q_mvar, slack, status in \
            zip(df.index, df.name, df.bus, df.p_mw, df.vm_pu, df.sn_mva, df.min_q_mvar, df.max_q_mvar, df.slack,
                df.in_service):
        gen_dict[gen_index] = {}
        gen_dict[gen_index]['name'] = name
        gen_name_list.append(gen_dict[gen_index]['name'])
        gen_dict[gen_index]['con_bus'] = bus_dict[bus]['bus_name']
        gen_dict[gen_index]['mon_bus'] = bus_dict[bus]['bus_name']
        gen_dict[gen_index]['P'] = p_mw
        gen_dict[gen_index]['Q'] = 0
        gen_dict[gen_index]['VIMP'] = vm_pu
        gen_dict[gen_index]['SNOM'] = sn_mva
        gen_dict[gen_index]['Qmin'] = min_q_mvar
        gen_dict[gen_index]['Qmax'] = max_q_mvar
        gen_dict[gen_index]['status'] = check_status(status)
        # check for slack bus
        if slack == True:
            slack_bus_record = f"SLACK\t{gen_dict[gen_index]['name']}\t;\n"
            slack_record_list.append(slack_bus_record)

    # Static generators
    df = net.sgen
    try:
        for sgen_index, name, bus, p_mw, q_mvar, sn_mva, status in zip(df.index, df.name, df.bus, df.p_mw, df.q_mvar,
                                                                       df.sn_mva, df.in_service):
            sgen_dict[sgen_index] = {}
            sgen_dict[sgen_index]['name'] = name
            sgen_name_list.append(sgen_dict[sgen_index]['name'])
            sgen_dict[sgen_index]['con_bus'] = bus_dict[bus]['bus_name']
            sgen_dict[sgen_index]['mon_bus'] = bus_dict[bus]['bus_name']
            sgen_dict[sgen_index]['P'] = p_mw
            sgen_dict[sgen_index]['Q'] = q_mvar
            sgen_dict[sgen_index]['SNOM'] = sn_mva
            sgen_dict[sgen_index]['status'] = check_status(status)
            sgen_dict[sgen_index]['VIMP'] = 0
            sgen_dict[sgen_index]['Qmin'] = 0
            sgen_dict[sgen_index]['Qmax'] = 0
    except:
        pass

    # External Grid
    try:
        df = net.ext_grid
        for ext_grid_index, bus, vm_pu, va_degree, in_service, in zip(df.index, df.bus, df.vm_pu, df.va_degree,
                                                                      df.in_service):
            ext_grid_dict[ext_grid_index] = {}
            ext_grid_dict[ext_grid_index]['name'] = "Ext_Grid"
            ext_grid_dict[ext_grid_index]['con_bus'] = bus_dict[bus]['bus_name']
            ext_grid_dict[ext_grid_index]['vm_pu'] = vm_pu
            ext_grid_dict[ext_grid_index]['status'] = check_status(in_service)
            # check for slack bus
            slack_bus_record = f"SLACK\t{ext_grid_dict[ext_grid_index]['con_bus']}\t;\n"
            slack_record_list.append(slack_bus_record)
    except:
        pass

    # Switches
    df = net.switch
    try:
        for switch_index, bus, element, et, closed, name in zip(df.index, df.bus, df.element, df.et, df.closed,
                                                                df.name):
            if et == 'b':
                switch_dict[switch_index] = {}
                switch_dict[switch_index]['name'] = name
                switch_name_list.append(switch_dict[switch_index]['name'])
                switch_dict[switch_index]['first_bus'] = bus_dict[bus]['bus_name']
                switch_dict[switch_index]['second_bus'] = bus_dict[element]['bus_name']
                switch_dict[switch_index]['status'] = check_status(closed)
            else:
                wrong_switch_type = True
    except:
        pass
    if wrong_switch_type:
        print("Artere supports only bus to bus switch")

    # Transformers
    df = net.trafo
    for trafo_index, name, hv_bus, lv_bus, sn_mva, vn_hv_kv, vn_lv_kv, vk_percent, vkr_percent, i0_percent, shift_degree, tap_side, tap_neutral, tap_min, tap_max, tap_step_percent, tap_step_degree, tap_pos, status in zip \
                (df.index, df.name, df.hv_bus, df.lv_bus, df.sn_mva, df.vn_hv_kv, df.vn_lv_kv, df.vk_percent,
                 df.vkr_percent, df.i0_percent, df.shift_degree, df.tap_side, df.tap_neutral, df.tap_min, df.tap_max,
                 df.tap_step_percent, df.tap_step_degree, df.tap_pos, df.in_service):
        trafo_dict[trafo_index] = {}
        trafo_dict[trafo_index]['name'] = name
        trafo_name_list.append(trafo_dict[trafo_index]['name'])
        trafo_dict[trafo_index]['from_bus'] = bus_dict[lv_bus]['bus_name']
        trafo_dict[trafo_index]['to_bus'] = bus_dict[hv_bus]['bus_name']
        trafo_dict[trafo_index]['hv_bus'] = hv_bus
        trafo_dict[trafo_index]['lv_bus'] = lv_bus
        trafo_dict[trafo_index]['PHI'] = shift_degree
        trafo_dict[trafo_index]['sn_mva'] = sn_mva

        # find R, X, C
        zk = vk_percent
        rk = vkr_percent
        xk = math.sqrt(pow(zk, 2) - pow(rk, 2))

        B = i0_percent / 100
        trafo_dict[trafo_index]['X'] = xk
        trafo_dict[trafo_index]['R'] = rk
        trafo_dict[trafo_index]['B'] = B

        # Con bus
        if tap_side == "hv":
            Con_Bus = bus_dict[hv_bus]['bus_name']
            trafo_dict[trafo_index]['con_bus'] = Con_Bus
        elif tap_side == "lv":
            Con_Bus = bus_dict[lv_bus]['bus_name']
            trafo_dict[trafo_index]['con_bus'] = Con_Bus
        elif tap_side == None:
            trafo_dict[trafo_index]['con_bus'] = "\' \'"

        # TAPS
        # Number of positions
        try:
            trafo_dict[trafo_index]['NBPOS'] = (tap_max - tap_min + 1)
        except:
            trafo_dict[trafo_index]['NBPOS'] = 0
        if pd.isnull(tap_max):
            trafo_dict[trafo_index]['NBPOS'] = 0

        # First & Last
        if tap_step_percent == 0:
            N_First = 0
            N_Last = 0
        else:  # abs
            N_First = 100 - (tap_neutral - (tap_min)) * tap_step_percent
            N_Last = (tap_max - tap_neutral) * tap_step_percent + 100

        # N ratio
        if pd.isnull(tap_pos) or tap_pos == 0:  # If tap position is zero or null, Nratio is 100%
            trafo_dict[trafo_index]['N_ratio'] = 100
        else:
            trafo_dict[trafo_index]['N_ratio'] = (tap_pos - tap_neutral) * tap_step_percent + 100
            # tap_step_percent * (tap_neutral - tap_pos) + 100

        if tap_pos == tap_min and tap_pos == tap_max:
            N_First = N_Last = 0
            trafo_dict[trafo_index]['con_bus'] = "\' \'"
            trafo_dict[trafo_index]['NBPOS'] = 0

        trafo_dict[trafo_index]['N_First'] = N_First
        trafo_dict[trafo_index]['N_Last'] = N_Last

        if pd.isnull(N_First):
            trafo_dict[trafo_index]['N_First'] = 0
        if pd.isnull(N_Last):
            trafo_dict[trafo_index]['N_Last'] = 0

        trafo_dict[trafo_index]['status'] = check_status(status)

    create_dat_file(filename)


def create_dat_file(filename):
    # Buses
    for index in range(len(bus_dict)):
        bus_record = f"BUS\t{bus_dict[index]['bus_name']}\t{bus_dict[index]['vn_kv']}\t{bus_dict[index].get('Pload', 0)}\t{bus_dict[index].get('Qload', 0)}\t{bus_dict[index].get('Bshunt', 0)}\t{bus_dict[index].get('Qshunt', 0)}\t;\n"
        bus_record_list.append(bus_record)

    # lines
    for index in range(len(line_dict)):
        line_record = f"LINE\t{line_dict[index]['name']}\t{line_dict[index]['from_bus']}\t{line_dict[index]['to_bus']}\t{line_dict[index]['Resistance']}\t{line_dict[index]['Reactance']}\t{line_dict[index]['half_shunt_susceptance']}\t{line_dict[index].get('Snom', 0)}\t{line_dict[index]['status']}\t;\n"
        line_record_list.append(line_record)

    # Generators
    for index in range(len(gen_dict)):
        gen_record = f"GENER\t{gen_dict[index]['name']}\t{gen_dict[index]['con_bus']}\t{gen_dict[index]['mon_bus']}\t{gen_dict[index]['P']}\t{gen_dict[index]['Q']}\t{gen_dict[index]['VIMP']}\t{gen_dict[index]['SNOM']}\t{gen_dict[index]['Qmin']}\t{gen_dict[index]['Qmax']}\t{gen_dict[index]['status']};\n"
        gen_record_list.append(gen_record)

    # Static Generators
    for index in range(len(sgen_dict)):
        sgen_record = f"GENER\t{sgen_dict[index]['name']}\t{sgen_dict[index]['con_bus']}\t{sgen_dict[index]['mon_bus']}\t{sgen_dict[index]['P']}\t{sgen_dict[index]['Q']}\t0\t{sgen_dict[index]['SNOM']}\t{sgen_dict[index]['Qmin']}\t{sgen_dict[index]['Qmax']}\t{sgen_dict[index]['status']}\t;\n"
        sgen_record_list.append(sgen_record)

    # External Grid
    for index in range(len(ext_grid_dict)):
        ext_grid_record = f"GENER\t{ext_grid_dict[index]['name']}\t{ext_grid_dict[index]['con_bus']}\t{ext_grid_dict[index]['con_bus']}\t9999\t9999\t{ext_grid_dict[index]['vm_pu']}\t9999\t-9990\t9999\t{ext_grid_dict[index]['status']}\t;\n"
        ext_grid_list.append(ext_grid_record)

    # Transformers  TRFO
    for index in range(len(trafo_dict)):
        transfo_record = f"TRFO\t{trafo_dict[index]['name']}\t{trafo_dict[index]['from_bus']}\t{trafo_dict[index]['to_bus']}\t{trafo_dict[index]['con_bus']}\t{trafo_dict[index]['R']}\t{trafo_dict[index]['X']}\t{trafo_dict[index]['B']}\t{trafo_dict[index]['N_ratio']}\t{trafo_dict[index]['sn_mva']}\t{trafo_dict[index]['N_First']}\t{trafo_dict[index]['N_Last']}\t{trafo_dict[index]['NBPOS']}\t0\t0\t{trafo_dict[index]['status']}\t;\n"
        trafo_record_list.append(transfo_record)


    # Switches
    for index in range(len(switch_dict)):
        switch_record = f"SWITCH\t{switch_dict[index]['name']}\t{switch_dict[index]['first_bus']}\t{switch_dict[index]['second_bus']}\t{switch_dict[index]['status']}\t;\n"
        switch_record_list.append(switch_record)

    dat_file = filename + ".dat"
    dat_file = dat_file.replace(" ", "_")

    print(dat_file)
    with open(dat_file, 'w') as Artere_file:
        for bus in bus_record_list:
            Artere_file.write(bus)

        for line in line_record_list:
            Artere_file.write(line)

        for transformer in trafo_record_list:
            Artere_file.write(transformer)

        for generator in gen_record_list:
            Artere_file.write(generator)

        for sgen in sgen_record_list:
            Artere_file.write(sgen)

        for ext_grid in ext_grid_list:
            Artere_file.write(ext_grid)

        for switch in switch_record_list:
            Artere_file.write(switch)

        for slack in slack_record_list:
            Artere_file.write(slack)

        Artere_file.write(f'FNOM\t{frequency}\t;\n')
