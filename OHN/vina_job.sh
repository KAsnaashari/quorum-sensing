for i in 1 2 3 4 5
do
	vina --receptor ../QscR/3szt.pdbqt --ligand OHN.pdbqt --out vina_results/3szt_OHN_1024_$i.pdbqt --config OHN_vina_config.conf
done
