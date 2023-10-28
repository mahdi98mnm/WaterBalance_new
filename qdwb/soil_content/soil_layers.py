import pandas as pd
import numpy as np

def waterSoilContentNotCoverd(
    infiltration: float,
    evaporation: float,
    init_swc_evaporation_layer: float,
    init_swc_transition_layer: float,
    z_evaporation_layer: float,
    z_transition_layer: float,
    fc_evaporation_layer: float,
    fc_transition_layer: float,
    pwp_evaporation_layer: float,
    pwp_transition_layer: float
):
    
    # current soil water content of Evaporation Layer:-------------------------------------------------------------------------------------------
    
    fc_evaporation_layer = fc_evaporation_layer *  z_evaporation_layer / 100

    pwp_evaporation_layer = pwp_evaporation_layer *  z_evaporation_layer / 100
    
    if init_swc_evaporation_layer < pwp_evaporation_layer:
        
        init_swc_evaporation_layer = pwp_evaporation_layer
    
    temp_1 = init_swc_evaporation_layer + infiltration - evaporation
    
    if temp_1 >= fc_evaporation_layer:
        
        current_evaporation_layer_to_transition_layer = temp_1 - fc_evaporation_layer
      
        current_swc_evaporation_layer = fc_evaporation_layer
        
    
    elif temp_1 <= pwp_evaporation_layer:

        evaporation = evaporation - (pwp_evaporation_layer - temp_1)
        
        current_swc_evaporation_layer = pwp_evaporation_layer
        
        # TODO: Fix this line
        current_evaporation_layer_to_transition_layer = 0
        

    else:
        
        current_swc_evaporation_layer = temp_1
        
        # TODO: Fix this line
        current_evaporation_layer_to_transition_layer = 0
        
        
    
    # current soil water content of Transition Layer:-------------------------------------------------------------------------------------------
    
    fc_transition_layer = fc_transition_layer * z_transition_layer / 100

    pwp_transition_layer = pwp_transition_layer *  z_transition_layer / 100
    
    if init_swc_transition_layer < pwp_transition_layer:
        
        init_swc_transition_layer = pwp_transition_layer
       
    temp_2 = init_swc_transition_layer + current_evaporation_layer_to_transition_layer  

    if temp_2 >= fc_transition_layer:
        
        deepPercolation = temp_2 - fc_transition_layer
        
        current_swc_transition_layer = fc_transition_layer 
             
    
    elif temp_2 <= pwp_transition_layer:
        
        current_swc_transition_layer = pwp_transition_layer
        
        # TODO: Fix this line
        # current_evaporation_layer_to_transition_layer = current_evaporation_layer_to_transition_layer - (pwp_transition_layer - temp_2)
        
        deepPercolation = 0
        
    else:
        
        current_swc_transition_layer = temp_2
        
        # TODO: Fix this line
        # current_evaporation_layer_to_transition_layer = 0

        deepPercolation = 0

    # -------------------------------------------------------------------------------------------

    # t_evaporation = (current_swc_evaporation_layer - pwp_evaporation_layer) / (fc_evaporation_layer - pwp_evaporation_layer)
    # t_transition = (current_swc_transition_layer - pwp_transition_layer) / (fc_transition_layer - pwp_transition_layer)
    # alpha = t_evaporation - t_transition
    # current_evaporation_layer_to_transition_layer = alpha * hydraulic_conductivity_of_evaporation_to_transition_layer


    return current_swc_evaporation_layer, current_swc_transition_layer, current_evaporation_layer_to_transition_layer, deepPercolation, evaporation, temp_2





def waterSoilContentCoverd(
    infiltration: float,
    evaporation: float,
    transpiration : float,
    init_swc_evaporation_layer: float,
    init_swc_transition_layer: float,
    init_swc_transpiration_layer : float,
    z_evaporation_layer: float,
    z_transition_layer: float,
    z_transpiration_layer: float,
    fc_evaporation_layer: float,
    fc_transition_layer: float,
    fc_transpiration_layer: float,
    pwp_evaporation_layer: float,
    pwp_transition_layer: float,
    pwp_transpiration_layer: float,
    stress_coefficient : float = 1,
    MAD: float = 0
):

    # current soil water content of Evaporation Layer:-------------------------------------------------------------------------------------------
        
    fc_evaporation_layer = fc_evaporation_layer *  z_evaporation_layer / 100

    pwp_evaporation_layer = pwp_evaporation_layer *  z_evaporation_layer / 100
    
    if init_swc_evaporation_layer < pwp_evaporation_layer:
        
        init_swc_evaporation_layer = pwp_evaporation_layer
    
    temp_1 = init_swc_evaporation_layer + infiltration - evaporation
    
    if temp_1 >= fc_evaporation_layer:
        
        current_evaporation_layer_to_transpiration_layer = temp_1 - fc_evaporation_layer
    
        current_swc_evaporation_layer = fc_evaporation_layer
        
    
    elif temp_1 <= pwp_evaporation_layer:
        
        
        evaporation = evaporation - (pwp_evaporation_layer - temp_1)
        
        current_swc_evaporation_layer = pwp_evaporation_layer

        
        # TODO: Fix this line
        current_evaporation_layer_to_transpiration_layer = 0
        

    else:
        
        current_swc_evaporation_layer = temp_1
        
        # TODO: Fix this line
        current_evaporation_layer_to_transpiration_layer = 0

    
    # current soil water content of Transpiration Layer:-------------------------------------------------------------------------------------------
    
    fc_transpiration_layer = fc_transpiration_layer * z_transpiration_layer / 100

    pwp_transpiration_layer = pwp_transpiration_layer *  z_transpiration_layer / 100
    
    if init_swc_transpiration_layer < pwp_transpiration_layer:
        
        init_swc_transpiration_layer = pwp_transpiration_layer
       
    temp_2 = init_swc_transpiration_layer + current_evaporation_layer_to_transpiration_layer - transpiration

    fc_transpiration_layer_for_deficit_irrigation = fc_transpiration_layer * stress_coefficient

    available_water = fc_transpiration_layer - pwp_transpiration_layer


    if temp_2 >= fc_transpiration_layer:
        
        current_transpiration_layer_to_transition_layer = temp_2 - fc_transpiration_layer
        
        current_swc_transpiration_layer = fc_transpiration_layer 

        irrigation_requirement = 0
             
    
    elif temp_2 <= pwp_transpiration_layer:


        transpiration = transpiration - (pwp_transpiration_layer - temp_2)

        irrigation_requirement = fc_transpiration_layer_for_deficit_irrigation - temp_2

        current_swc_transpiration_layer = pwp_transpiration_layer

        
        
        
        
        # TODO: Fix this line
        # current_evaporation_layer_to_transpiration_layer = current_evaporation_layer_to_transpiration_layer

        current_transpiration_layer_to_transition_layer = 0

        
        
    else:
        
        current_swc_transpiration_layer_in_MAD = fc_transpiration_layer - (MAD * available_water)

        if current_swc_transpiration_layer_in_MAD >= temp_2:
            
            irrigation_requirement = fc_transpiration_layer - temp_2

            current_swc_transpiration_layer = fc_transpiration_layer

            # TODO: Fix this line
            
            
            current_transpiration_layer_to_transition_layer = 0

        else:
            irrigation_requirement = 0


            # TODO: Fix this line
            
            
            current_transpiration_layer_to_transition_layer = 0
            current_swc_transpiration_layer = temp_2
    

    # current soil water content of Transition Layer:-------------------------------------------------------------------------------------------
    
    fc_transition_layer = fc_transition_layer * z_transition_layer / 100

    pwp_transition_layer = pwp_transition_layer *  z_transition_layer / 100
    
    if init_swc_transition_layer < pwp_transition_layer:
        
        init_swc_transition_layer = pwp_transition_layer
       
    temp_3 = init_swc_transition_layer + current_transpiration_layer_to_transition_layer  

    if temp_3 >= fc_transition_layer:
        
        deepPercolation = temp_3 - fc_transition_layer
        
        current_swc_transition_layer = fc_transition_layer 
             
    
    elif temp_3 <= pwp_transition_layer:
        
        current_swc_transition_layer = pwp_transition_layer
        
        # TODO: Fix this line
        # current_transpiration_layer_to_transition_layer = current_transpiration_layer_to_transition_layer
        deepPercolation = 0
        
    else:
        
        current_swc_transition_layer = temp_3
        
        # TODO: Fix this line
        # current_transpiration_layer_to_transition_layer = current_transpiration_layer_to_transition_layer
        deepPercolation = 0

    # -------------------------------------------------------------------------------------------

    # t_evaporation = (current_swc_evaporation_layer - pwp_evaporation_layer) / (fc_evaporation_layer - pwp_evaporation_layer)
    # t_transition = (current_swc_transition_layer - pwp_transition_layer) / (fc_transition_layer - pwp_transition_layer)
    # t_transpiration = (current_swc_transition_layer - pwp_transpiration_layer) / (fc_transpiration_layer_with_stress - pwp_transpiration_layer)

    # alpha_1 = t_evaporation - t_transpiration
    # alpha_2 = t_transpiration - t_transition

    # current_evaporation_layer_to_transpiration_layer = alpha_1 * hydraulic_conductivity_of_evaporation_to_transpiration_layer
    # current_transpiration_layer_to_transition_layer = alpha_2 * hydraulic_conductivity_of_transpiration_to_transition_layer


    return current_swc_evaporation_layer, current_swc_transpiration_layer, current_swc_transition_layer, current_evaporation_layer_to_transpiration_layer, current_transpiration_layer_to_transition_layer, transpiration, evaporation, irrigation_requirement, deepPercolation





def waterSoilContentAlayer(
    infiltration: float,
    evapotraspiration : float,
    init_swc_evaporation_layer: float,
    z_evaporation_layer: float,
    fc_evaporation_layer: float,
    pwp_evaporation_layer: float,
    stress_coefficient : float = 1,
    MAD: float = 0.5
):
    
    fc_evaporation_layer = fc_evaporation_layer *  z_evaporation_layer / 100

    pwp_evaporation_layer = pwp_evaporation_layer *  z_evaporation_layer / 100
    
    if init_swc_evaporation_layer < pwp_evaporation_layer:
        
        init_swc_evaporation_layer = pwp_evaporation_layer
    
    temp = init_swc_evaporation_layer + infiltration - evapotraspiration

    fc_evaporation_layer_with_stress = fc_evaporation_layer * stress_coefficient
    
    if temp >= fc_evaporation_layer_with_stress:
        
        deepPercolation = temp - fc_evaporation_layer_with_stress
    
        current_swc_evaporation_layer = fc_evaporation_layer_with_stress

        irrigation_requirement = 0
        
    
    elif temp <= pwp_evaporation_layer:

        evapotraspiration = evapotraspiration - (pwp_evaporation_layer - temp)
        
        current_swc_evaporation_layer = pwp_evaporation_layer


        irrigation_requirement = fc_evaporation_layer_with_stress - current_swc_evaporation_layer

        
        
        # TODO: Fix this line
        deepPercolation = 0
        

    else:
        current_swc_evaporation_layer_in_MAD = MAD * (temp - pwp_evaporation_layer)

        if current_swc_evaporation_layer_in_MAD >= temp:

            irrigation_requirement = fc_evaporation_layer_with_stress - temp

            current_swc_evaporation_layer = fc_evaporation_layer_with_stress
        
        
            # TODO: Fix this line
            deepPercolation = 0

        else:
            irrigation_requirement = 0

            # TODO: Fix this line
            deepPercolation = 0
            current_swc_evaporation_layer = temp

    
    return current_swc_evaporation_layer, irrigation_requirement, deepPercolation, evapotraspiration
    
   






def waterSoilContent(
    covered : int,
    infiltration: float,
    evaporation: float,
    init_swc_evaporation_layer: float,
    init_swc_transition_layer: float,
    z_evaporation_layer: float,
    z_transition_layer: float,
    fc_evaporation_layer: float,
    fc_transition_layer: float,
    pwp_evaporation_layer: float,
    pwp_transition_layer: float,
    stress_coefficient : float = 1,
    MAD: float = 0,
    transpiration : float = None,
    init_swc_transpiration_layer : float = None,
    pwp_transpiration_layer: float = None,
    z_transpiration_layer: float = None,
    fc_transpiration_layer: float = None
):
    if covered == 2:
        
        current_evaporation_layer_to_transition_layer = np.nan
        # current soil water content of Evaporation Layer:-------------------------------------------------------------------------------------------
        
        fc_evaporation_layer = fc_evaporation_layer *  z_evaporation_layer / 100

        pwp_evaporation_layer = pwp_evaporation_layer *  z_evaporation_layer / 100
        
        if init_swc_evaporation_layer < pwp_evaporation_layer:
            
            init_swc_evaporation_layer = pwp_evaporation_layer
        
        temp_1 = init_swc_evaporation_layer + infiltration - evaporation
        
        if temp_1 >= fc_evaporation_layer:
            
            current_evaporation_layer_to_transpiration_layer = temp_1 - fc_evaporation_layer
        
            current_swc_evaporation_layer = fc_evaporation_layer
            
        
        elif temp_1 <= pwp_evaporation_layer:
            
            if evaporation > pwp_evaporation_layer - temp_1 :
                
                return_evaporation = (pwp_evaporation_layer - temp_1) - evaporation
                
                evaporation = evaporation + return_evaporation
            
            current_swc_evaporation_layer = pwp_evaporation_layer

            
            # TODO: Fix this line
            current_evaporation_layer_to_transpiration_layer = 0
            

        else:
            
            current_swc_evaporation_layer = temp_1
            
            # TODO: Fix this line
            current_evaporation_layer_to_transpiration_layer = 0

        
        # current soil water content of Transpiration Layer:-------------------------------------------------------------------------------------------
        
        fc_transpiration_layer = fc_transpiration_layer * z_transpiration_layer / 100

        pwp_transpiration_layer = pwp_transpiration_layer *  z_transpiration_layer / 100
        
        if init_swc_transpiration_layer < pwp_transpiration_layer:
            
            init_swc_transpiration_layer = pwp_transpiration_layer
        
        temp_2 = init_swc_transpiration_layer + current_evaporation_layer_to_transpiration_layer - transpiration

        fc_transpiration_layer_for_deficit_irrigation = fc_transpiration_layer * stress_coefficient

        available_water = fc_transpiration_layer - pwp_transpiration_layer


        if temp_2 >= fc_transpiration_layer:
            
            current_transpiration_layer_to_transition_layer = temp_2 - fc_transpiration_layer
            
            current_swc_transpiration_layer = fc_transpiration_layer 

            irrigation_requirement = 0
                
        
        elif temp_2 <= pwp_transpiration_layer:

            if transpiration > pwp_transpiration_layer - temp_2 :
                
                return_transpiration = (pwp_transpiration_layer - temp_2) - transpiration
                
                transpiration = transpiration + return_transpiration
                

            irrigation_requirement = fc_transpiration_layer_for_deficit_irrigation - temp_2

            current_swc_transpiration_layer = pwp_transpiration_layer

            
            
            
            
            # TODO: Fix this line
            # current_evaporation_layer_to_transpiration_layer = current_evaporation_layer_to_transpiration_layer

            current_transpiration_layer_to_transition_layer = 0

            
            
        else:
            
            current_swc_transpiration_layer_in_MAD = fc_transpiration_layer - (MAD * available_water)

            if current_swc_transpiration_layer_in_MAD >= temp_2:
                
                irrigation_requirement = fc_transpiration_layer - temp_2

                current_swc_transpiration_layer = fc_transpiration_layer

                # TODO: Fix this line
                
                
                current_transpiration_layer_to_transition_layer = 0

            else:
                irrigation_requirement = 0


                # TODO: Fix this line
                
                
                current_transpiration_layer_to_transition_layer = 0
                current_swc_transpiration_layer = temp_2
        

        # current soil water content of Transition Layer:-------------------------------------------------------------------------------------------
        
        fc_transition_layer = fc_transition_layer * z_transition_layer / 100

        pwp_transition_layer = pwp_transition_layer *  z_transition_layer / 100
        
        if init_swc_transition_layer < pwp_transition_layer:
            
            init_swc_transition_layer = pwp_transition_layer
        
        temp_3 = init_swc_transition_layer + current_transpiration_layer_to_transition_layer  

        if temp_3 >= fc_transition_layer:
            
            deepPercolation = temp_3 - fc_transition_layer
            
            current_swc_transition_layer = fc_transition_layer 
                
        
        elif temp_3 <= pwp_transition_layer:
            
            current_swc_transition_layer = pwp_transition_layer
            
            # TODO: Fix this line
            # current_transpiration_layer_to_transition_layer = current_transpiration_layer_to_transition_layer
            deepPercolation = 0
            
        else:
            
            current_swc_transition_layer = temp_3
            
            # TODO: Fix this line
            # current_transpiration_layer_to_transition_layer = current_transpiration_layer_to_transition_layer
            deepPercolation = 0

        # -------------------------------------------------------------------------------------------
    
    elif covered == 1 :
        
        current_swc_transpiration_layer = np.nan
        current_evaporation_layer_to_transpiration_layer = np.nan
        current_transpiration_layer_to_transition_layer = np.nan
        transpiration = np.nan
        irrigation_requirement = np.nan
        
        # current soil water content of Evaporation Layer:-------------------------------------------------------------------------------------------
        
        fc_evaporation_layer = fc_evaporation_layer *  z_evaporation_layer / 100

        pwp_evaporation_layer = pwp_evaporation_layer *  z_evaporation_layer / 100
        
        if init_swc_evaporation_layer < pwp_evaporation_layer:
            
            init_swc_evaporation_layer = pwp_evaporation_layer
        
        temp_1 = init_swc_evaporation_layer + infiltration - evaporation
        
        if temp_1 >= fc_evaporation_layer:
            
            current_evaporation_layer_to_transition_layer = temp_1 - fc_evaporation_layer
        
            current_swc_evaporation_layer = fc_evaporation_layer
            
        
        elif temp_1 <= pwp_evaporation_layer:
            
            if evaporation > pwp_evaporation_layer - temp_1 :
                
                return_evaporation = (pwp_evaporation_layer - temp_1) - evaporation
                
                evaporation = evaporation + return_evaporation
            
            current_swc_evaporation_layer = pwp_evaporation_layer
            
            # TODO: Fix this line
            current_evaporation_layer_to_transition_layer = 0
            

        else:
            
            current_swc_evaporation_layer = temp_1
            
            # TODO: Fix this line
            current_evaporation_layer_to_transition_layer = 0
            
            
        
        # current soil water content of Transition Layer:-------------------------------------------------------------------------------------------
        
        fc_transition_layer = fc_transition_layer * z_transition_layer / 100

        pwp_transition_layer = pwp_transition_layer *  z_transition_layer / 100
        
        if init_swc_transition_layer < pwp_transition_layer:
            
            init_swc_transition_layer = pwp_transition_layer
        
        temp_2 = init_swc_transition_layer + current_evaporation_layer_to_transition_layer  

        if temp_2 >= fc_transition_layer:
            
            deepPercolation = temp_2 - fc_transition_layer
            
            current_swc_transition_layer = fc_transition_layer 
                
        
        elif temp_2 <= pwp_transition_layer:
            
            current_swc_transition_layer = pwp_transition_layer
            
            # TODO: Fix this line
            # current_evaporation_layer_to_transition_layer = current_evaporation_layer_to_transition_layer - (pwp_transition_layer - temp_2)
            
            deepPercolation = 0
            
        else:
            
            current_swc_transition_layer = temp_2
            
            # TODO: Fix this line
            # current_evaporation_layer_to_transition_layer = 0

            deepPercolation = 0

        # -------------------------------------------------------------------------------------------
    else:
        current_swc_evaporation_layer = np.nan
        current_swc_transpiration_layer = np.nan
        current_swc_transition_layer = np.nan
        current_evaporation_layer_to_transpiration_layer = np.nan
        current_evaporation_layer_to_transition_layer = np.nan
        current_transpiration_layer_to_transition_layer = np.nan
        transpiration = np.nan
        evaporation = evaporation
        irrigation_requirement = np.nan
        deepPercolation = np.nan
        
    return current_swc_evaporation_layer, current_swc_transpiration_layer, current_swc_transition_layer, current_evaporation_layer_to_transpiration_layer,current_evaporation_layer_to_transition_layer ,current_transpiration_layer_to_transition_layer, transpiration, evaporation, irrigation_requirement, deepPercolation
        
        
        
        