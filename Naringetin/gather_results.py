import sys, getopt
import pandas as pd

atomic_mass = {'O': 15.999, 'C': 12.0107, 'N': 14.0067, 'H': 1.00784}

ligand_name = ''
n = 0
try:
	opts, args = getopt.getopt(sys.argv[1:], 'l:')
except getopt.GetoptError:
	print('Invalid arguments: gather_results.py -l ligand_name')
	sys.exit(2)
for arg, opt in opts:
	if arg == '-h':
		print('gather_results.py -l ligand_name')
		sys.exit(0)
	elif arg == '-l':
		ligand_name = opt
data = {
	'ligand': [], 
	'score': [], 
	'COM_x': [], 
	'COM_y': [], 
	'COM_z': [], 
	'exhaustiveness': [], 
	'i': [],
	'model': []
}
add_atoms = True
with open(f'vina_results/3szt_2048.pdbqt', 'r') as results_file:
	print(f'vina_results/3szt_2048.pdbqt...')
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
			data['exhaustiveness'].append(2048)
			data['i'].append(1)
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
for i in range(5):
	with open(f'vina_results/3szt_{ligand_name}_8192_{i+1}.pdbqt', 'r') as results_file:
		print(f'vina_results/3szt_{ligand_name}_8192_{i+1}.pdbqt...')
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
				data['exhaustiveness'].append(8192)
				data['i'].append(i+1)
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
df.to_csv('vina_results.csv', index=False)
print(f'Results gathered in vina_results.csv')
