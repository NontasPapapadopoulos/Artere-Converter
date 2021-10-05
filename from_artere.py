"""
The aim of this program is to convert a .dat file which is used for the ARTERE program.
This program reads and grabs the data from the .dat file and creates a Python file in order
to make a network with pandapower.
"""
import math
import shlex

busList = []
init_vm_pu_list = []
init_va_degree_list = []
load_list = []
generatorList = []
transformersList = []
linesList = []
switchList = []
shuntsList = []
busDict = {}
bus_voltage_dict = {}
genDict = {}
recordList = []
controllersList = []




def checkStatus(element_status):
    if element_status == 1:
        return True
    return False


def from_artere(inputFile):
    records = ""
    global frequency
    frequency = 50

    with open(inputFile) as artereFile:
        lines = artereFile.readlines()
        for record in lines:
            if record[0][0] == "#" or record[0][0] == "!":
                pass
            else:
                records += record.rstrip()

    for line in records.split(";"):
        if line:
            recordList.append(shlex.split(line))

    for record in recordList:
        if record[0] == 'SLACK':
            slackBus = record[1]

        if record[0] == 'FNOM':
            frequency = float(record[1])


    for record in recordList:
        if record[0] == 'BUS':
            bus_name = record[1]
            vn_kv = float(record[2])
            Pload = float(record[3])
            Qload = float(record[4])
            Bshunt = float(record[5])
            Qshunt = float(record[6])

            # List of bus names
            try:
                bus_name = bus_name.replace(" ", "_")
            except:
                pass

            # Create a bus
            busDict[bus_name] = {}
            busDict[bus_name]["name"] = bus_name
            busDict[bus_name]["voltage"] = vn_kv

            # Create a string that is going to be stored in the Python file.
            created_bus = f"{bus_name} = pp.create_bus(net, vn_kv={vn_kv}, name=\"{bus_name}\", in_service=True)\n"
            busList.append(created_bus)

            # If the bus has a load, create a load connected to the bus.
            if Pload != 0 or Qload != 0:
                created_load = f"pp.create_load(net, bus={bus_name}, p_mw={Pload}, q_mvar={Qload}, name=\"{bus_name}\", in_service=True)\n"
                load_list.append(created_load)

            # if the bus has a shunt, create a shunt to the bus
            # Qshunt-> Create load, Bshunt-> Create shunt
            if Qshunt != 0:
                created_load = f"pp.create_load(net, bus={bus_name}, name=\"{bus_name}_Shunt\", p_mw=0, q_mvar={Qshunt}, in_service=True) \n"
                load_list.append(created_load)
            if Bshunt != 0:
                created_shunt = f"pp.create_shunt(net, bus={bus_name}, q_mvar={Bshunt}, in_service=True)\n"
                shuntsList.append(created_shunt)

        # Transmittion lines
        if record[0] == 'LINE':
            line_name = record[1]
            from_bus = record[2]
            to_bus = record[3]
            R_Ohm = float(record[4])
            X_Ohm = float(record[5])
            half_shunt_suceptance = float(record[6]) / 10 ** 6  # It is given in μS
            Snom = float(record[7])
            status = checkStatus(int(record[8]))



            if Snom == 0:
                Snom = 9999

            # Calculate the maximum curent
            line_voltage = busDict[from_bus]["voltage"]
            Imax = (Snom * 10 ** 6) / (math.sqrt(3) * line_voltage * 10 ** 3)
            Imax = Imax / 1000
            Imax = format(Imax, '.6f')

            # Calculate the capacitance in nF.  ωC/2
            Capacitance = (half_shunt_suceptance * 2) / (2 * math.pi * frequency)
            Capacitance = Capacitance * 10 ** 9  # nF
            Capacitance = format(Capacitance, '.6f')

            created_line = f'pp.create_line_from_parameters(net, from_bus={busDict[from_bus]["name"]}, to_bus={busDict[to_bus]["name"]}, name="{line_name}"' \
                           f', length_km=1, r_ohm_per_km={R_Ohm}, x_ohm_per_km={X_Ohm}, max_i_ka={Imax}, c_nf_per_km={Capacitance}, in_service={status})\n'
            linesList.append(created_line)

        # LTC-V
        if record[0] == 'LTC-V':
            print('LTC-V is not supported. ')
            raise Warning('LTC-V is not supported.')

        # Transformers for TRANSFO record
        if record[0] == 'TRANSFO':
            transfo_name = record[1]
            from_bus = record[2]
            to_bus = record[3]
            rk = float(record[4]) # Resistance Ohm
            xk = float(record[5]) # Reactance
            SusceptanceB1 = float(record[6])
            SusceptanceB2 = float(record[7])
            N_ratio = float(record[8])
            ym = (SusceptanceB1 + SusceptanceB2) / 2.0
            Snom = float(record[10])
            status = int(record[11])
            PHI = float(record[9])


            status = checkStatus(status)

            # vk, vkr, i0_percent

            vk_percent = math.sqrt(pow(rk, 2) + pow(xk, 2))  # zk
            vkr_percent = rk
            i0_percent = ym

            # Check which bus is High level and which is low.
            if busDict[from_bus]['voltage'] > busDict[to_bus]['voltage']:
                high_lvl_bus = from_bus
                low_lvl_bus = to_bus
            else:
                high_lvl_bus = to_bus
                low_lvl_bus = from_bus

            if N_ratio > 100:
                tap_neutral = 0
                tap_min = N_ratio - 100
                tap_max = N_ratio - 100
                tap_pos = N_ratio - 100
                tap_step_percent = 1
                tap_side = "\"hv\""

            elif N_ratio < 100:
                tap_neutral = 0
                tap_min = -100 + N_ratio
                tap_max = -100 + N_ratio
                tap_pos = -100 + N_ratio
                tap_step_percent = 1
                tap_side = "\"hv\""

            # Create a transformer
            # if the ratio is not 100, we should take into account the taps.
            if N_ratio == 100:
                created_transformer = f'pp.create_transformer_from_parameters(net, hv_bus={busDict[high_lvl_bus]["name"]}, lv_bus={busDict[low_lvl_bus]["name"]}, sn_mva={Snom}, ' \
                                      f'name=\"{transfo_name}\", shift_degree={PHI}, vn_hv_kv={busDict[high_lvl_bus]["voltage"]}, vn_lv_kv={busDict[low_lvl_bus]["voltage"]}, vkr_percent={vkr_percent}, vk_percent={vk_percent}, pfe_kw=0, i0_percent={i0_percent}, in_service={status})\n'
            else:
                created_transformer = f'pp.create_transformer_from_parameters(net, hv_bus={busDict[high_lvl_bus]["name"]}, lv_bus={busDict[low_lvl_bus]["name"]}, sn_mva={Snom}, name={transfo_name}, ' \
                                      f'shift_degree={PHI}, vn_hv_kv={busDict[high_lvl_bus]["voltage"]}, vn_lv_kv={busDict[low_lvl_bus]["voltage"]}, vkr_percent={vkr_percent}, vk_percent={vk_percent},' \
                                      f' pfe_kw=0, i0_percent={i0_percent}, tap_min={tap_min}, tap_max={tap_max}, tap_step_percent={tap_step_percent}, tap_pos={tap_pos},tap_neutral={tap_neutral}, tap_side={tap_side}, in_service={status})\n'

            transformersList.append(created_transformer)

        # Transformer for TRFO record
        if record[0] == 'TRFO':
            transfo_name = record[1]
            from_bus = record[2]
            to_bus = record[3]
            CON_BUS = record[4]
            Ohm_Resistance = (record[5])

            if CON_BUS == '\'' and Ohm_Resistance == '\'':
                CON_BUS = None
                Ohm_Resistance = float(record[6])
                Xreactance = float(record[6 + 1])
                Susceptance = float(record[7 + 1])
                N_ratio = float(record[8 + 1])
                Snom = float(record[9 + 1])
                N_First = float(record[10 + 1]) * 100
                N_Last = float(record[11 + 1]) * 100
                NBPOS = int(float(record[12 + 1]))
                TOLV = record[13 + 1]
                VDES = record[14 + 1]
                On_off = int(record[15 + 1])
            else:
                Ohm_Resistance = float(record[5])
                Xreactance = float(record[6])
                Susceptance = float(record[7])
                N_ratio = float(record[8])
                Snom = float(record[9])
                N_First = float(record[10])
                N_Last = float(record[11])
                NBPOS = int(float(record[12]))
                TOLV = record[13]
                VDES = record[14]
                On_off = int(record[15])

            status = checkStatus(On_off)


            # if TOLV != "0" and VDES != "0":
            #     CreateController = f"ContinuousTapControl(net, tid, vm_set_pu={VDES}, tol={TOLV}, side='{tap_side}', trafotype='2W', in_service=True) \n"
            #     controllersList.append(CreateController)

            # vkr, vk, i0 percent
            Ym = Susceptance
            rk = Ohm_Resistance
            xk = Xreactance
            zk = math.sqrt(pow(rk, 2) + pow(xk, 2))
            vk_percent = zk
            vkr_percent = rk
            i0_percent = Ym

            # Check which bus is High level and which is low.
            if busDict[from_bus]["voltage"] > busDict[to_bus]["voltage"]:
                high_lvl_bus = from_bus
                low_lvl_bus = to_bus
            else:
                high_lvl_bus = to_bus
                low_lvl_bus = from_bus

            # TAPS
            try:
                if CON_BUS.isdigit():
                    CON_BUS = "b" + CON_BUS
            except:
                pass

            try:
                if busDict[CON_BUS]['voltage'] == busDict[high_lvl_bus]['voltage']:
                    tap_side = "\"hv\""
                elif busDict[CON_BUS]['voltage'] == busDict[low_lvl_bus]['voltage']:
                    tap_side = "\"lv\""
                else:
                    tap_side = None
            except:
                tap_side = None

            # tap_max = NBPOS, tap_min=0
            # check if the N ratio is not 100, while NBPOS, N_first and N_Last are 0.
            if N_ratio != 100 and NBPOS == 0 and N_First == 0 and N_Last == 0:
                if N_ratio > 100:
                    tap_neutral = 0
                    tap_min = N_ratio - 100
                    tap_max = N_ratio - 100
                    tap_pos = N_ratio - 100
                    tap_step_percent = 1
                    tap_side = "\"hv\""

                elif N_ratio < 100:
                    tap_neutral = 0
                    tap_min = -100 + N_ratio
                    tap_max = -100 + N_ratio
                    tap_pos = -100 + N_ratio
                    tap_step_percent = 1
                    tap_side = "\"lv\""

                # Create a string
                created_transformer = f'pp.create_transformer_from_parameters(net, hv_bus={busDict[high_lvl_bus]["name"]}, lv_bus={busDict[low_lvl_bus]["name"]}, sn_mva={Snom}, name="{transfo_name}", ' \
                                      f'vn_hv_kv={busDict[high_lvl_bus]["voltage"]}, vn_lv_kv={busDict[low_lvl_bus]["voltage"]}, vkr_percent={vkr_percent}, vk_percent={vk_percent}, pfe_kw=0, i0_percent={i0_percent}, ' \
                                      f'tap_pos={tap_pos}, tap_neutral={tap_neutral}, tap_step_percent={tap_step_percent}, tap_side={tap_side}, tap_min={tap_min}, tap_max={tap_max}, in_service={status})\n'

                transformersList.append(created_transformer)

            # if N_ratio , N_First, N_last are equal:
            elif N_ratio != 100 and N_First == N_Last and N_Last == N_ratio:
                if N_ratio > 100:
                    tap_neutral = 0
                    tap_min = N_ratio - 100
                    tap_max = N_ratio - 100
                    tap_pos = N_ratio - 100
                    tap_step_percent = 1
                    # tap_side = "\"hv\""

                elif N_ratio < 100:
                    tap_neutral = 0
                    tap_min = -100 + N_ratio
                    tap_max = -100 + N_ratio
                    tap_pos = -100 + N_ratio
                    tap_step_percent = 1
                    # tap_side = "\"lv\""

                # Create a string
                created_transformer = f'pp.create_transformer_from_parameters(net, hv_bus={busDict[high_lvl_bus]["name"]}, lv_bus={busDict[low_lvl_bus]["name"]}, sn_mva={Snom}, name="{transfo_name}", ' \
                                      f'vn_hv_kv={busDict[high_lvl_bus]["voltage"]}, vn_lv_kv={busDict[low_lvl_bus]["voltage"]}, vkr_percent={vkr_percent}, vk_percent={vk_percent}, pfe_kw=0, i0_percent={i0_percent}, ' \
                                      f'tap_pos={tap_pos}, tap_neutral={tap_neutral}, tap_step_percent={tap_step_percent}, tap_side={tap_side}, tap_min={tap_min}, tap_max={tap_max}, in_service={status})\n'

                # Store the string to a list
                transformersList.append(created_transformer)

            elif N_ratio == 100 and N_First == 0 and N_Last == 0:
                # Create a string
                created_transformer = f'pp.create_transformer_from_parameters(net, hv_bus={busDict[high_lvl_bus]["name"]}, lv_bus={busDict[low_lvl_bus]["name"]}, sn_mva={Snom}, name="{transfo_name}", ' \
                                      f'vn_hv_kv={busDict[high_lvl_bus]["voltage"]}, vn_lv_kv={busDict[low_lvl_bus]["voltage"]}, vkr_percent={vkr_percent}, vk_percent={vk_percent}, pfe_kw=0, ' \
                                      f'i0_percent={i0_percent}, in_service={status})\n'

                # Store the string to a list
                transformersList.append(created_transformer)

            elif N_ratio > 0 and N_First > 0 and N_Last > 0 and NBPOS > 0:

                tap_step_percent = (N_Last - N_First) / (NBPOS - 1)

                tap_neutral = (100 - float(N_First)) / tap_step_percent
                tap_neutral = round(tap_neutral)

                tap_pos = (float(N_ratio) - N_First) / tap_step_percent
                tap_pos = round(tap_pos)

                created_transformer = f'pp.create_transformer_from_parameters(net, hv_bus={busDict[high_lvl_bus]["name"]}, lv_bus={busDict[low_lvl_bus]["name"]}, sn_mva={Snom}, name="{transfo_name}", ' \
                                      f'vn_hv_kv={busDict[high_lvl_bus]["voltage"]}, vn_lv_kv={busDict[low_lvl_bus]["voltage"]}, vkr_percent={vkr_percent}, vk_percent={vk_percent}, pfe_kw=0, i0_percent={i0_percent}, ' \
                                      f'tap_pos={tap_pos}, tap_neutral={tap_neutral}, tap_step_percent={tap_step_percent}, tap_side={tap_side}, tap_min=0, tap_max={NBPOS - 1}, in_service={status})\n'

                transformersList.append(created_transformer)

        # Generators
        if record[0] == 'GENER':
            gener_name = record[1]
            bus_connected = record[2]
            Pproduction = float(record[4])
            Qproduction = float(record[5])
            Snom = record[7]
            VIMP = record[6]
            Qmin = float(record[8])
            Qmax = float(record[9])
            On_off = int(record[10])

            # Check if it is in service
            status = checkStatus(On_off)

            # if VIMP is zero, the generator is treated as a PQ bus (we create sgen)
            # Otherwise it is treated as a PV bus and the Q is ignored
            if VIMP == "0":
                created_sgen = f'pp.create_sgen(net, bus={busDict[bus_connected]["name"]}, p_mw={Pproduction}, q_mvar={Qproduction}, sn_mva={Snom}, name="{gener_name}", max_q_mvar={Qmax}, min_q_mvar={Qmin}, in_service={status})\n'
                generatorList.append(created_sgen)

            else:
                if gener_name == slackBus:
                    created_gen = f'pp.create_gen(net, p_mw={Pproduction}, max_q_mvar={Qmax}, min_q_mvar={Qmin}, sn_mva={Snom}, bus={busDict[bus_connected]["name"]}, vm_pu={VIMP}, name="{gener_name}", slack={True}, in_service={status})\n'
                    generatorList.append(created_gen)

                elif gener_name == "Ext_Grid":
                    created_gen = f'pp.create_gen(net, p_mw={Pproduction}, max_q_mvar={Qmax}, min_q_mvar={Qmin}, sn_mva={Snom}, bus={busDict[bus_connected]["name"]}, vm_pu={VIMP}, name="{gener_name}", slack={True}, in_service={status})\n'
                    generatorList.append(created_gen)

                else:
                    created_gen = f'pp.create_gen(net, p_mw={Pproduction}, max_q_mvar={Qmax}, min_q_mvar={Qmin}, sn_mva={Snom}, bus={busDict[bus_connected]["name"]}, vm_pu={VIMP}, name="{gener_name}", slack={False}, in_service={status})\n'
                    generatorList.append(created_gen)

        # Switches
        if record[0] == 'SWITCH':
            switch_name = record[1]
            first_bus = record[2]
            second_bus = record[3]
            On_off = int(record[4])

            status = checkStatus(On_off)

            created_switch = f'pp.create_switch(net, bus={busDict[first_bus]["name"]}, name="{switch_name}" ,element={second_bus}, et="b" ,closed={status})\n'
            switchList.append(created_switch)

        # LFRESV specifies the voltage magnitude and phase at a bus.
        if record[0] == 'LFRESV':
            init_vm_pu = float(record[2])  # Voltage magnitude in pu  # MODULE
            init_va_degree = float(record[3])  # Phase angle in radians   # PHASE

            init_vm_pu_list.append(init_vm_pu)
            init_va_degree_list.append(init_va_degree)

    createNewFile(inputFile)


def createNewFile(file):
    # Those lines get the removes the .dat extension and puts .py
    newPythonFile = file.split('.')[0] + ".py"

    with open(newPythonFile, 'w') as pythonFile:
        pythonFile.write(f"""import pandapower as pp 
from pandapower.control.controller.trafo.ContinuousTapControl import ContinuousTapControl

net = pp.create_empty_network(f_hz={frequency}, sn_mva={100})
    
    """)
        pythonFile.write('\n# list of Buses:\n')
        for bus in busList:
            pythonFile.write(bus)

        pythonFile.write('\n\n# list of Loads:\n')
        for load in load_list:
            pythonFile.write(load)

        pythonFile.write('\n\n# List of Shunts:\n')
        for shunt in shuntsList:
            pythonFile.write(shunt)

        pythonFile.write('\n\n# list of Lines:\n')
        for line in linesList:
            pythonFile.write(line)

        pythonFile.write('\n\n# list of Transformers:\n')
        for transformer in transformersList:
            pythonFile.write(transformer)

        pythonFile.write('\n\n# list of Generators:\n')
        for generator in generatorList:
            pythonFile.write(generator)

        pythonFile.write('\n\n# List of Switches:\n')
        for switch in switchList:
            pythonFile.write(switch)

        pythonFile.write('\n\n# List of controllers:\n')
        for controller in controllersList:
            pythonFile.write(controller)

        pythonFile.write(f"""
init_va_degree_list = {init_va_degree_list} 
init_vm_pu_list = {init_vm_pu_list}
    
    
# Run power flow
if len(init_va_degree_list) > 0 and len(init_vm_pu_list) > 0:
    pp.runpp(net, init_va_degree=init_va_degree_list, init_vm_pu=init_vm_pu_list)
else:
    pp.runpp(net)
    
    
print(net.res_bus)          # bus results
""")
