import pandas as pd

ligands = ['Apigenin', 'Baicalin', 'Chrysin', 'Naringetin', 'Phloretin', 'Quercetin']

ligand_data = []
for ligand in ligands:
	ligand_data.append(pd.read_csv(f'{ligand}/vina_results.csv'))

dock_data = pd.concat(ligand_data)
dock_data.reset_index(inplace=True)
dock_data.drop('index', axis=1, inplace=True)
dock_data.to_csv('vina_results.csv')
