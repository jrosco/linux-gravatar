#!/bin/sh

# Set Build Directory
app_name="linux-gravatar"
build_number="1.1.1"
dist_dir="dist"
build_dir="build"
package_dir="packages"
os_arch="x86_64"

# Clean build directory
sudo rm -rf ${dist_dir} || echo "${dist_dir} does not exist. skipping"
sudo rm -rf ${build_dir} || echo "${build_dir} does not exist. skipping"

# Build dist
python3 setup.py bdist
tar xvf ${dist_dir}/${app_name}-${build_number}.linux-${os_arch}.tar.gz -C ${dist_dir}

# Copy Files
mkdir -p ${dist_dir}/DEBIAN
sudo cp data/DEBIAN/control ${dist_dir}/DEBIAN/

# Run DEB Builder
sudo dpkg-deb --build ${dist_dir}/

# Rename DEB File
mv dist.deb ${app_name}-${build_number}.linux-${os_arch}.deb

# Build a RPM (requires alien installed)
sudo alien -r ${app_name}-${build_number}.linux-${os_arch}.deb

# Move packages file
mkdir ${package_dir}
mv ./*.deb ${package_dir}/
mv ./*.rpm ${package_dir}/

# Cleanup
rm -rf ${build_dir} ${dist_dir}
