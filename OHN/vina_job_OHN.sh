for j in 0 1 2 3 
do
	for i in 1 2 3 4 5
	do
		vina --receptor ../QscR/3szt.pdbqt --ligand OHN.pdbqt --out vina_results/3szt_OHN_site$j\_1024_$i.pdbqt --config ../vina_config_site$j.conf
	done
done
