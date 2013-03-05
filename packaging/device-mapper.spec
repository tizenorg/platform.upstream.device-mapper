%define device_mapper_version 1.02.77
%define lvm2_version 2.02.98

# Do not reset Release to 1 unless both lvm2 and device-mapper
# versions are increased together.

Name:           device-mapper
Version:        1.02.77
Release:        1
License:        GPL-2.0
Summary:        Device mapper utility
Url:            http://sources.redhat.com/dm
Group:          System/Base
Source0:        ftp://sources.redhat.com/pub/lvm2/LVM2.%{lvm2_version}.tgz
Requires:       libdevmapper = %{device_mapper_version}-%{release}

%description
This package contains the supporting userspace utility, dmsetup,
for the kernel device-mapper.

%package devel
License:        LGPL-2.1
Summary:        Development libraries and headers for device-mapper
Group:          Development/Libraries
Requires:       %{name} = %{device_mapper_version}-%{release}
Requires:       libdevmapper = %{device_mapper_version}-%{release}

%description -n device-mapper-devel
This package contains files needed to develop applications that use
the device-mapper libraries.

%package -n libdevmapper
License:        LGPL-2.1
Summary:        Device-mapper shared library
Group:          System/Libraries
Obsoletes:      device-mapper < 1.02.17-6

%description -n libdevmapper
This package contains the device-mapper shared library, libdevmapper.

%prep
%setup -q -n LVM2.%{lvm2_version}

%build
%define _exec_prefix ""
%configure --with-user= --with-group= --with-device-uid=0 --with-device-gid=6 --with-device-mode=0660 --enable-pkgconfig
%define _exec_prefix /
make device-mapper

%install
make install_device-mapper DESTDIR=%{buildroot} usrlibdir=%{buildroot}/usr/%{_lib}
sed -i 's/ (.*)//g' %{buildroot}%{_libdir}/pkgconfig/*.pc


%post -n libdevmapper -p /sbin/ldconfig

%postun -n libdevmapper -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%license COPYING COPYING.LIB
%attr(755,root,root) %{_sbindir}/dmsetup
%{_mandir}/man8/dmsetup.8.gz

%files devel
%defattr(-,root,root,-)
%attr(755,root,root) /%{_libdir}/libdevmapper.so
%{_includedir}/libdevmapper.h
%{_libdir}/pkgconfig/*.pc

%files -n libdevmapper
%attr(755,root,root) /%{_libdir}/libdevmapper.so.*


