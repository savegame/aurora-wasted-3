%define __requires_exclude ^libmpg123.*\\.so.*|libopenal\\.so.*$
%define __provides_exclude_from ^%{_datadir}/%{name}/lib/.*\\.so.*$

Name:       ru.sashikknox.re3
Summary:    RE3
Release:    1
Version:    1.0.0
Group:      Amusements/Games
License:    GPLv3
Source0:    %{name}.tar.gz

BuildRequires: systemd-devel
BuildRequires: pkgconfig(openal)
BuildRequires: pkgconfig(libmpg123)
BuildRequires: pkgconfig(sndfile)
BuildRequires: pkgconfig(vorbis)
BuildRequires: pkgconfig(wayland-client)
BuildRequires: pkgconfig(wayland-cursor)
BuildRequires: pkgconfig(wayland-egl)
BuildRequires: pkgconfig(wayland-protocols)
BuildRequires: pkgconfig(wayland-scanner)
BuildRequires: pkgconfig(glesv2)
BuildRequires: pkgconfig(xkbcommon)
BuildRequires: pkgconfig(egl)
BuildRequires: pkgconfig(dbus-1)
BuildRequires: ninja
BuildRequires: cmake
BuildRequires: extra-cmake-modules
BuildRequires: patchelf

%description
RE3 - its open source GTA 3 Engine

%prep
%setup -q -n %{name}-%{version}

%build
mkdir -p build/%{_arch}/glfw
cmake \
    -G Ninja \
    -DCMAKE_MAKE_PROGRAM=/usr/bin/ninja \
    -DGLFW_LIBRARY_TYPE=STATIC \
    -DCMAKE_BUILD_TYPE=Release \
    -DGLFW_BUILD_WAYLAND=ON \
    -DGLFW_BUILD_X11=OFF \
    -DGLFW_STANDALONE=OFF \
    -DGLFW_AURORAOS=ON \
    -DGLFW_BUILD_EXAMPLES=OFF \
    -DGLFW_BUILD_TESTS=OFF \
    -DGLFW_BUILD_DOCS=OFF \
    -DCMAKE_INSTALL_PREFIX=build/%{_arch}/glfw.install \
    -Bbuild/%{_arch}/glfw \
    -Sglfw
cmake --build build/%{_arch}/glfw
cmake --install build/%{_arch}/glfw

mkdir -p build/%{_arch}/re3
env CMAKE_PREFIX_PATH=build/%{_arch}/glfw.install:$CMAKE_PREFIX_PATH \
    cmake \
        -G Ninja \
        -DCMAKE_MAKE_PROGRAM=/usr/bin/ninja \
        -DCMAKE_BUILD_TYPE=Release \
        -Bbuild/%{_arch}/re3 \
        -DLIBRW_PLATFORM=GL3 \
        -DLIBRW_GL3_GFXLIB=GLFW \
        -DAURORAOS=YES \
        -DAURORAOS_SHARED_DATA="%{_datadir}/%{name}/data" \
        -DRE3_INSTALL=YES \
        -DRE3__WITH_OPUS=YES \
        -DRE3__WITH_LIBSNDFIL=YES \
        -DGIT_SHA1="%{version}-AuroraOS" \
        -DCMAKE_INSTALL_PREFIX=build/%{_arch}/re3.install \
        -Sre3
cmake --build build/%{_arch}/re3
# cmake --install build/%{_arch}/re3

%install
rm -rf %{buildroot}
install -m 0655 -D ./aurora/icon_86.png %{buildroot}/usr/share/icons/hicolor/86x86/apps/%{name}.png
install -m 0655 -D ./aurora/icon_108.png %{buildroot}/usr/share/icons/hicolor/108x108/apps/%{name}.png
install -m 0655 -D ./aurora/icon_128.png %{buildroot}/usr/share/icons/hicolor/128x128/apps/%{name}.png
install -m 0655 -D ./aurora/icon_172.png %{buildroot}/usr/share/icons/hicolor/172x172/apps/%{name}.png
# install -m 0755 -D build/%{_arch}/re3.install/re3 %{buildroot}%{_bindir}/%{name}
install -m 0755 -D build/%{_arch}/re3/src/re3 %{buildroot}%{_bindir}/%{name}
patchelf --force-rpath --set-rpath %{_datadir}/%{name}/lib %{buildroot}%{_bindir}/%{name}
install -m 0755 -D %{_libdir}/libmpg123.so.0* -t %{buildroot}%{_datadir}/%{name}/lib/
install -m 0755 -D %{_libdir}/libopenal.so.1* -t %{buildroot}%{_datadir}/%{name}/lib/
install -m 0655 -D re3/gamefiles/gamecontrollerdb.txt -t %{buildroot}%{_datadir}/%{name}/data
install -m 0655 -D re3/gamefiles/data/* -t %{buildroot}%{_datadir}/%{name}/data/data
install -m 0655 -D re3/gamefiles/models/* -t %{buildroot}%{_datadir}/%{name}/data/models
install -m 0655 -D re3/gamefiles/neo/* -t %{buildroot}%{_datadir}/%{name}/data/neo
install -m 0655 -D re3/gamefiles/TEXT/* -t %{buildroot}%{_datadir}/%{name}/data/TEXT
install -m 0655 -D aurora/poster.png %{buildroot}%{_datadir}/%{name}/poster.png
install -m 0655 -D aurora/re3.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%defattr(-,root,root,-)
%attr(755,root,root) %{_bindir}/%{name}
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
