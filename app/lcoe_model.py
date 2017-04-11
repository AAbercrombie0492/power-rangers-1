import numpy as np

def lcoe_model(size_kw, esc, expected_yield_yr1, lifespan, degradation, soiling_yield_impact, coating_yield_impact, coating_om_impact, coating_cost_per_m2, coating_year, module_watts, module_area, **kwargs):
    
    coating_year = int(min(coating_year, lifespan ))
    
    module_watt_density = module_watts/module_area

    # Installed cost range
    inst_cost_avg = size_kw * 5096.17271 * size_kw**-0.09956
    inst_cost_min = inst_cost_avg - size_kw * 1038.47732 * size_kw**-0.04102
    inst_cost_max = inst_cost_avg + size_kw * 1038.47732 * size_kw**-0.04102

    # Fixed OM cost per year
    om_cost_avg = size_kw * 22.88422 * size_kw**-0.03543
    om_cost_min = om_cost_avg - size_kw * 28.28427 * size_kw**-0.1195
    om_cost_max = om_cost_avg + size_kw * 28.28427 * size_kw**-0.1195

    total_inst_cost      = inst_cost_avg
    total_inst_cost_dev = total_inst_cost - inst_cost_min

    pre_om_s       = np.ones(lifespan)*om_cost_avg
    pre_om_dev_s   = np.ones(lifespan)*(om_cost_avg - om_cost_min)

    pre_om_npv     = np.npv(esc, pre_om_s)
    pre_om_dev_npv = np.npv(esc, pre_om_dev_s)


    coating_cost_s                = np.zeros(lifespan)
    coating_cost_s[coating_year] = size_kw*1e3/module_watt_density*coating_cost_per_m2
    coating_cost_npv              = np.npv(esc, coating_cost_s)
    post_om_s                     = np.ones(lifespan)*om_cost_avg
    post_om_s[coating_year:]     *= 1 - coating_om_impact
    post_om_npv                   = np.npv(esc, post_om_s)
    post_om_dev_s                 = np.ones(lifespan)*(om_cost_avg - om_cost_min)
    post_om_dev_s[coating_year:] *= 1 - coating_om_impact
    post_om_dev_npv               = np.npv(esc, post_om_dev_s)

    yield_s             = expected_yield_yr1 * (1-degradation)**np.arange(lifespan)
    total_yield         = np.sum(yield_s)
    soiling_yield_s     = yield_s * (1 - soiling_yield_impact)
    total_soiling_yield = np.sum(soiling_yield_s)
    coating_yield_s     = soiling_yield_s * (1 - coating_yield_impact)
    total_coating_yield = np.sum(coating_yield_s)

    print total_yield, total_soiling_yield, total_coating_yield

    lcoe = {'none': {}, 'soil': {}, 'coat': {}}
    _high = (total_inst_cost + pre_om_npv + pre_om_dev_npv + total_inst_cost_dev)
    _avg = (total_inst_cost + pre_om_npv)
    _low = (total_inst_cost + pre_om_npv - pre_om_dev_npv - total_inst_cost_dev)
    lcoe['none']['high'] = _high / (size_kw * total_yield)
    lcoe['none']['avg']  = _avg / (size_kw * total_yield)
    lcoe['none']['low']  = _low / (size_kw * total_yield)

    lcoe['soil']['high'] = _high / (size_kw * total_soiling_yield)
    lcoe['soil']['avg']  = _avg / (size_kw * total_soiling_yield)
    lcoe['soil']['low']  = _low / (size_kw * total_soiling_yield)

    lcoe['coat']['high'] = _high / (size_kw * total_coating_yield)
    lcoe['coat']['avg']  = _avg / (size_kw * total_coating_yield)
    lcoe['coat']['low']  = _low / (size_kw * total_coating_yield)

    material_cost = coating_cost_s[coating_year]
    shifted_pre_om_npv = np.npv(esc, pre_om_s[coating_year:])
    shifted_post_om_npv = np.npv(esc, post_om_s[coating_year:])
    om_savings = shifted_pre_om_npv - shifted_post_om_npv
    net_savings = - material_cost + om_savings

    avg_savings_per_year = pre_om_s[coating_year] - post_om_s[coating_year]
    payback_period = material_cost / avg_savings_per_year

    lcoe['avg_savings_per_year'] = avg_savings_per_year
    lcoe['payback_periods'] = payback_period
    lcoe['material_cost'] = material_cost
    lcoe['om_savings'] = om_savings
    lcoe['net_savings'] = net_savings

    return lcoe


if __name__ == '__main__':
    size_kw = 1e4
    esc = 0.02
    expected_yield_yr1 = 1600.
    lifespan = 35
    degradation = 0.0025
    soiling_yield_impact = 0.1
    coating_yield_impact = 0.04
    coating_om_impact = 0.3
    coating_cost_per_m2 = 5.
    coating_year = 4
    module_watts = 290.
    module_area = 1.64007472

    lcoe = lcoe_model(size_kw, esc, expected_yield_yr1, lifespan, degradation,
               soiling_yield_impact, coating_yield_impact, coating_om_impact,
               coating_cost_per_m2, coating_year, module_watts, module_area)

    print("Done.")
