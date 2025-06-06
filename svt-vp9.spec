%define major 1
%define libpackage %mklibname svt-vp9 %{major}
%define devpackage %mklibname -d svt-vp9

%define oname   SVT-VP9

%define commit  f5039ec08465e21b15131f6bdc97bfa250ded1c9

# https://github.com/OpenVisualCloud/SVT-VP9/issues/159
ExclusiveArch:  %{x86_64}

Name:           svt-vp9
Version:        0.3.1
Release:        0.20250531.1
Summary:        Scalable Video Technology for VP9 Encoder
Group:          System/Libraries
License:        BSD-2-Clause-Patent and ISC
URL:            https://github.com/OpenVisualCloud/SVT-VP9
Source0:        https://github.com/OpenVisualCloud/SVT-VP9/archive/%{commit}.tar.gz

BuildRequires:  cmake
BuildRequires:  meson
BuildRequires:  yasm
BuildRequires:  help2man
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0)

Requires:	%{libpackage} = %{EVRD}
Requires: gstreamer1.0-%{name} = %{EVRD}

%description
The Scalable Video Technology for VP9 Encoder (SVT-VP9 Encoder)
is a VP9-compliant encoder library core. The SVT-VP9 Encoder development
is a work-in-progress targeting performance levels applicable to both VOD
and Live encoding/transcoding video applications.

%package -n %{libpackage}
Summary:    SVT-VP9 libraries
Group:		System/Libraries

%description -n %{libpackage}
This package contains SVT-VP9 libraries.

%package -n %{devpackage}
Summary:    Development files for SVT-VP9
Requires:	%{name} = %{EVRD}
Requires:	%{libpackage} = %{EVRD}

%description -n %{devpackage}
This package contains the development files for SVT-VP9.

%package -n     gstreamer1.0-%{name}
Summary:        GStreamer 1.0 %{name}-based plug-in
Requires:       gstreamer1.0-plugins-base

%description -n gstreamer1.0-%{name}
This package provides %{name}-based GStreamer plug-in.


%prep
%autosetup -p1 -n %{oname}-%{commit}
# Patch build gstreamer plugin
sed -e "s|install: true,|install: true, include_directories : [ include_directories('../Source/API') ], link_args : '-lSvtVp9Enc',|" \
-e "/svtvp9enc_dep =/d" -e 's|, svtvp9enc_dep||' -e "s|svtvp9enc_dep.found()|true|" -i gstreamer-plugin/meson.build

%build
%cmake \
    -DCMAKE_BUILD_TYPE=Release
%make_build

cd ..
export LIBRARY_PATH="$LIBRARY_PATH:$(pwd)/Bin/Release"
cd gstreamer-plugin
%meson
%meson_build
cd ..

%install
%make_install -C build
rm -f %{buildroot}%{_libdir}/*.{a,la}

pushd gstreamer-plugin
%meson_install
popd

%files
%doc Docs/*
%{_bindir}/SvtVp9EncApp

%files -n %{libpackage}
%license LICENSE.md
%doc README.md
%{_libdir}/libSvtVp9Enc.so.%{major}*

%files -n %{devpackage}
%{_includedir}/%{name}
%{_libdir}/libSvtVp9Enc.so
%{_libdir}/pkgconfig/*.pc

%files -n gstreamer1.0-%{name}
%{_libdir}/gstreamer-1.0/libgstsvtvp9enc.so
