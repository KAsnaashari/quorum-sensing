import sys, getopt
import pandas as pd

atomic_mass = {'O': 15.999, 'C': 12.0107, 'N': 14.0067, 'H': 1.00784}
ligands = ['Apigenin', 'Baicalin', 'Chrysin', 'Naringetin', 'Phloretin', 'Quercetin', 'OHN']

ligand_data = []
for ligand in ligands:
	ligand_name = ligand
	data = {
		'ligand': [], 
		'site': [],
		'score': [], 
		'COM_x': [], 
		'COM_y': [], 
		'COM_z': [], 
		'exhaustiveness': [], 
		'i': [],
		'model': []
	}
	for site in range(4):
		for i in range(5):
			with open(f'{ligand_name}/vina_results/3szt_{ligand_name}_site{site}_1024_{i+1}.pdbqt', 'r') as results_file:
				print(f'Reading {ligand_name}/vina_results/3szt_{ligand_name}_site{site}_1024_{i+1}.pdbqt...')
				lines = results_file.readlines()
				com_x = com_y = com_z = m_tot = model = 0
				for line in lines:
					w = line.split()
					if w[0] == 'ENDMDL':
						com_x /= m_tot
						com_y /= m_tot
						com_z /= m_tot
						data['COM_x'].append(com_x)
						data['COM_y'].append(com_y)
						data['COM_z'].append(com_z)
						data['exhaustiveness'].append(1024)
						data['i'].append(i+1)
						data['site'].append(site)
						data['model'].append(model)
					if w[0] == 'REMARK' and w[1] == 'VINA':
						data['score'].append(float(w[3]))
						data['ligand'].append(ligand_name)
						m_tot = com_x = com_y = com_z = 0
					elif w[0] == 'ATOM':
						atom = w[2][0]
						m = atomic_mass[atom]
						m_tot += m
						x = float(w[5])
						y = float(w[6])
						z = float(w[7])
						com_x += m * x
						com_y += m * y
						com_z += m * z 
					elif w[0] == 'MODEL':
						model = int(w[1])
	df = pd.DataFrame(data)
	df.to_csv(f'{ligand_name}/vina_sites_results.csv', index=False)
	print(f'Results gathered in {ligand_name}/vina_sites_results.csv')


ligand_data = []
for ligand in ligands:
	ligand_data.append(pd.read_csv(f'{ligand}/vina_sites_results.csv'))

dock_data = pd.concat(ligand_data)
dock_data.reset_index(inplace=True)
dock_data.drop('index', axis=1, inplace=True)
dock_data.to_csv('vina_sites_results.csv')
print('All site results gathered in vina_sites_results.csv')

