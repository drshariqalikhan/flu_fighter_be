
import json
import os
import pandas as pd


def infoAbout(strain):



    name = ""
    killRate = ""
    recovery_pd = ""
    hospitalizationRate = ""
    if(strain == 'AH1N12009_Chart01_CategoryGroup2_Chart01_CategoryGroup3_Value_DataValue0'):


        name = "Influenza A (H1N1)pdm09"
        killRate = "26 (range 11-66) per 100,000"
        recovery_pd = "10 days"
        hospitalizationRate = "1 in 1000"
    if(strain == 'AH3_Chart01_CategoryGroup2_Chart01_CategoryGroup3_Value_DataValue0'):

        name = "Influenza A (H3N2)"
        killRate = "1 in 100000"
        recovery_pd = "5 days"
        hospitalizationRate = "1 in 100000"

    if(strain == 'AH5_Chart01_CategoryGroup2_Chart01_CategoryGroup3_Value_DataValue0'):

        name = "Influenza A (H5) "
        killRate = "1 in 100000"
        recovery_pd = "5 days"
        hospitalizationRate = "1 in 100000"

    if(strain == 'AH1_Chart01_CategoryGroup2_Chart01_CategoryGroup3_Value_DataValue0'):

        name = "Influenza A (H1)"
        killRate = "1 in 100000"
        recovery_pd = "5 days"
        hospitalizationRate = "1 in 100000"

    if(strain == 'ANOTSUBTYPED_Chart01_CategoryGroup2_Chart01_CategoryGroup3_Value_DataValue0'):

        name = "Influenza A (not subtyped)"
        killRate = "1 in 100000"
        recovery_pd = "5 days"
        hospitalizationRate = "1 in 100000"

    if(strain == 'BYAMAGATA_Chart01_CategoryGroup2_Chart01_CategoryGroup3_Value_DataValue0'):

        name = "Type B Yamagata"
        killRate = "1 in 100000"
        recovery_pd = "5 days"
        hospitalizationRate = "1 in 100000"

    if(strain == 'BVICTORIA_Chart01_CategoryGroup2_Chart01_CategoryGroup3_Value_DataValue0'):

        name = "Type B Victoria"
        killRate = "1 in 100000"
        recovery_pd = "5 days"
        hospitalizationRate = "1 in 100000"

    if(strain == 'BNOTDETERMINED_Chart01_CategoryGroup2_Chart01_CategoryGroup3_Value_DataValue0'):

        name = "Type B (not subtyped)"
        killRate = "1 in 100000"
        recovery_pd = "5 days"
        hospitalizationRate = "1 in 100000"

    return {
            'name': name,
            'killRate': killRate,
            'recovery_pd': recovery_pd,
            'hospitalizationRate':hospitalizationRate
        }

def parseCsvFolder(folder_path,site_root):


    el = []
    for filename in folder_path:

        filepath = os.path.splitext(filename)[0]
        filename = os.path.join(site_root,'flucsv',filename)

        # print(filename)
        country = filepath.split('_')[0]
        alert = filepath.split('_')[1]
        try:


             #open csv
            df = pd.read_csv(filename,skiprows=3)
            # print(df)
            df = df.fillna(0)
            # #to get flu trend list



            df['total']= (

                df.AH5_Chart01_CategoryGroup2_Chart01_CategoryGroup3_Value_DataValue0
                + df.AH1_Chart01_CategoryGroup2_Chart01_CategoryGroup3_Value_DataValue0
                + df.AH1N12009_Chart01_CategoryGroup2_Chart01_CategoryGroup3_Value_DataValue0
                + df.AH3_Chart01_CategoryGroup2_Chart01_CategoryGroup3_Value_DataValue0
                + df.ANOTSUBTYPED_Chart01_CategoryGroup2_Chart01_CategoryGroup3_Value_DataValue0
                + df.BYAMAGATA_Chart01_CategoryGroup2_Chart01_CategoryGroup3_Value_DataValue0
                + df.BVICTORIA_Chart01_CategoryGroup2_Chart01_CategoryGroup3_Value_DataValue0
                + df.BNOTDETERMINED_Chart01_CategoryGroup2_Chart01_CategoryGroup3_Value_DataValue0)
            total_list =df['total'].tolist()
            total_list = [float(integral) for integral in total_list]
            bottom = df.tail(1)
            new_bottom = bottom.filter([
                'AH5_Chart01_CategoryGroup2_Chart01_CategoryGroup3_Value_DataValue0',
                'AH1_Chart01_CategoryGroup2_Chart01_CategoryGroup3_Value_DataValue0' ,
                'AH1N12009_Chart01_CategoryGroup2_Chart01_CategoryGroup3_Value_DataValue0',
                'AH3_Chart01_CategoryGroup2_Chart01_CategoryGroup3_Value_DataValue0',
                'ANOTSUBTYPED_Chart01_CategoryGroup2_Chart01_CategoryGroup3_Value_DataValue0',
                'BYAMAGATA_Chart01_CategoryGroup2_Chart01_CategoryGroup3_Value_DataValue0',
                'BVICTORIA_Chart01_CategoryGroup2_Chart01_CategoryGroup3_Value_DataValue0',
                'BNOTDETERMINED_Chart01_CategoryGroup2_Chart01_CategoryGroup3_Value_DataValue0'
                ],axis=1)

            new_bottom.reset_index(drop=True, inplace=True)

            main_strain = new_bottom.idxmax(axis = 1)
            main_strain = main_strain.tolist()[0]

            next_bottom = new_bottom.drop([main_strain],axis =1)
            other_strain = next_bottom.idxmax(axis = 1)
            other_strain = other_strain.tolist()[0]

            data_out = {

                'country_name': code_to_county(country),
                'country': country,
                'alert':alert,
                'trend':total_list,
                'main_strain':infoAbout(main_strain),
                'other_strain':infoAbout(other_strain)
            }

            el.append(data_out)
           
        except:
            pass
    # print (len(el))        

    return el        

  



def code_to_county(code):



    if (code == 'xAu'):
        return 'Australia'
    if (code == 'xAf'):
        return 'Central Africa'
    if (code == 'xAs'):
        return 'South-East Asia'
    if (code == 'xEu'):
        return 'South-East Europe'
    if (code == 'xSo'):
        return 'South America'
    if (code == 'xNo'):
        return 'North America'

    if (code == 'us'):
        return 'United States'        
    if (code == 'br'):
        return 'Brazil'
    if (code == 'cn'):
        return 'China'
    if (code == 'ru'):
        return 'Russia'
    if (code == 'id'):
        return 'Indonesia'
    if (code == 'in'):
        return 'India'
    if (code == 'jp'):
        return 'Japan'
    if (code == 'kr'):
        return 'South Korea'
    if (code == 'my'):
        return 'Malaysia'
    if (code == 'pk'):
        return 'Pakistan'
    if (code == 'sg'):
        return 'Singapore'
   