mkdir -p new_directory_name/sub_directory_name #creates new directory, sub-directory is optional



pwd #returns active working directory

ls #shows all file names in working directory
ls sub_directory_name #shos file names under sub-directory

cd new_working_directory
cd .. #exits to parent directory

source .venv/bin/activate
deactivate

pip instal requests numpy

my_variable="hello"
echo $my_variable