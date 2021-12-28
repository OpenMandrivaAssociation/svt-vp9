%define major 0
%define libpackage %mklibname svt-av1 %{major}
%define devpackage %mklibname -d svt-av1

%define oname   SVT-AV1

Name:           svt-av1
Version:        0.8.7
Release:        1
Summary:        Scalable Video Technology for AV1 Encoder
Group:          System/Libraries
License:        BSD and MIT and ISC and Public Domain
URL:            https://gitlab.com/AOMediaCodec/SVT-AV1
Source0:        https://gitlab.com/AOMediaCodec/SVT-AV1/-/archive/v%{version}/%{oname}-v%{version}.tar.bz2

BuildRequires:  cmake
BuildRequires:  meson
BuildRequires:  yasm
BuildRequires:  help2man
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0)

Requires:	%{libpackage} = %{EVRD}
Requires: gstreamer1.0-%{name} = %{EVRD}

%description
The Scalable Video Technology for AV1 Encoder (SVT-AV1 Encoder) is an
AV1-compliant encoder library core. The SVT-AV1 development is a
work-in-progress targeting performance levels applicable to both VOD and Live
encoding / transcoding video applications.

%package -n %{libpackage}
Summary:    SVT-AV1 libraries
Group:		System/Libraries

%description -n %{libpackage}
This package contains SVT-AV1 libraries.

%package -n %{devpackage}
Summary:    Development files for SVT-AV1
Requires:	%{name} = %{EVRD}
Requires:	%{libpackage} = %{EVRD}
Recommends: %{name}-devel-docs = %{EVRD}

%description -n %{devpackage}
This package contains the development files for SVT-AV1.

%package devel-docs
Summary:    Development documentation for SVT-AV1
BuildArch:  noarch

%description devel-docs
This package contains the documentation for development of SVT-AV1.

%package -n     gstreamer1.0-%{name}
Summary:        GStreamer 1.0 %{name}-based plug-in
Requires:       gstreamer1.0-plugins-base

%description -n gstreamer1.0-%{name}
This package provides %{name}-based GStreamer plug-in.

%prep
%autosetup -p1 -n %{oname}-v%{version}
# Patch build gstreamer plugin
sed -e "s|install: true,|install: true, include_directories : [ include_directories('../Source/API') ], link_args : '-lSvtAv1Enc',|" \
-e "/svtav1enc_dep =/d" -e 's|, svtav1enc_dep||' -e "s|svtav1enc_dep.found()|true|" -i gstreamer-plugin/meson.build

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

install -d -m0755 %{buildroot}/%{_mandir}/man1
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:%{buildroot}%{_libdir}
help2man -N --help-option=-help --version-string=%{version} %{buildroot}%{_bindir}/SvtAv1DecApp > %{buildroot}%{_mandir}/man1/SvtAv1DecApp.1
help2man -N --help-option=-help --no-discard-stderr --version-string=%{version} %{buildroot}%{_bindir}/SvtAv1EncApp > %{buildroot}%{_mandir}/man1/SvtAv1EncApp.1

pushd gstreamer-plugin
%meson_install
popd

%files
%{_bindir}/SvtAv1DecApp
%{_bindir}/SvtAv1EncApp
%{_mandir}/man1/SvtAv1DecApp.1*
%{_mandir}/man1/SvtAv1EncApp.1*

%files -n %{libpackage}
%license LICENSE.md PATENTS.md
%doc CHANGELOG.md CONTRIBUTING.md README.md
%{_libdir}/libSvtAv1Dec.so.%{major}*
%{_libdir}/libSvtAv1Enc.so.%{major}*

%files -n %{devpackage}
%{_includedir}/%{name}
%{_libdir}/libSvtAv1Dec.so
%{_libdir}/libSvtAv1Enc.so
%{_libdir}/pkgconfig/SvtAv1Dec.pc
%{_libdir}/pkgconfig/SvtAv1Enc.pc

%files devel-docs
%license LICENSE.md PATENTS.md
%doc Docs

%files -n gstreamer1.0-%{name}
%{_libdir}/gstreamer-1.0/libgstsvtav1enc.so
