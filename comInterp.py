def compress_interp(Dict_interpolated_V1_tp1, Dict_interpolated_C1_tp1, Dict_interpolated_V2_tp1, Dict_interpolated_C2_tp1, Dict_interpolated_V3_tp1, Dict_interpolated_C3_tp1, Dict_interpolated_V5_tp1, Dict_interpolated_C5_tp1):
    Dict_interp = {}
    Dict_interp['V'] = {}
    Dict_interp['V'][1] = Dict_interpolated_V1_tp1
    Dict_interp['V'][2] = Dict_interpolated_V2_tp1
    Dict_interp['V'][3] = Dict_interpolated_V3_tp1
    Dict_interp['V'][5] = Dict_interpolated_V5_tp1
    Dict_interp['C'] = {}
    Dict_interp['C'][1] = Dict_interpolated_C1_tp1
    Dict_interp['C'][2] = Dict_interpolated_C2_tp1
    Dict_interp['C'][3] = Dict_interpolated_C3_tp1
    Dict_interp['C'][5] = Dict_interpolated_C5_tp1
    return Dict_interp


