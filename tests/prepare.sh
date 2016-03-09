#~/bin/bash
if [[ "$(basename -- "$0")" = "prepare.sh" ]]; then
	echo "Please only source this script"
	exit 1
fi

# Write basic configuration
cp ../example.conf mcwrapper.conf

if [[ $PREPARED != "y" ]]; then
	# Move to known directory
	cd "$( dirname "${BASH_SOURCE[0]}" )"

	if [[ $MCSERVERS == "y" ]]; then
		mkdir -p minecraft-server
		echo "eula=true" > minecraft-server/eula.txt
		# Get Minecraft 1.8.8
		[ -f minecraft-server/minecraft_server.1.8.8.jar ] || \
			wget https://s3.amazonaws.com/Minecraft.Download/versions/1.8.8/minecraft_server.1.8.8.jar -O minecraft-server/minecraft_server.1.8.8.jar
		# Get Minecraft 1.9
		[ -f minecraft-server/minecraft_server.1.9.jar ] || \
			wget https://s3.amazonaws.com/Minecraft.Download/versions/1.9/minecraft_server.1.9.jar -O minecraft-server/minecraft_server.1.9.jar
		function mcservers_clean {
			find minecraft-server | tail -n +2 | egrep -v "minecraft_server.*jar" | egrep -v "eula.txt" | xargs rm -rf
		}
	fi

	export PATH=$( realpath .. ):$PATH
	export PREPARED="y"
fi
