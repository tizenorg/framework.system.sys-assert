Name:       sys-assert
Summary:    libsys-assert (shared object).
Version:    0.3.2
Release:    10
Group:      Framework/system
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:	%{name}.manifest
Source101:	packaging/tizen-debug-on.service
Source102:	packaging/tizen-debug-off.service

BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(libunwind)
BuildRequires:	cmake
Requires:	libunwind
Requires(post): coreutils
Requires(post): smack-utils

%description
libsys-assert (shared object).

%prep
%setup -q
cp %{SOURCE1} .

%build
%if 0%{?sec_build_binary_crash_enable}
export CFLAGS+=" -DTIZEN_ENABLE_COREDUMP"
%endif
export CFLAGS+=" -fPIC -Werror"
%ifarch %{arm}
	export CFLAGS+=" -DARM"
%else
	%ifarch %{ix86}
    	export CFLAGS+=" -DX86"
	%endif
%endif

cmake . -DCMAKE_INSTALL_PREFIX=/usr

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install
mkdir -p %{buildroot}/usr/share/license
cp LICENSE %{buildroot}/usr/share/license/%{name}
mkdir -p %{buildroot}%{_libdir}/systemd/system/sysinit.target.wants
install -m 0644 %{SOURCE101} %{buildroot}%{_libdir}/systemd/system/tizen-debug-on.service
install -m 0644 %{SOURCE102} %{buildroot}%{_libdir}/systemd/system/tizen-debug-off.service
ln -s ../tizen-debug-on.service %{buildroot}%{_libdir}/systemd/system/sysinit.target.wants/tizen-debug-on.service
ln -s ../tizen-debug-off.service %{buildroot}%{_libdir}/systemd/system/sysinit.target.wants/tizen-debug-off.service

%post
/sbin/ldconfig
if [ ! -d /.build ]; then
	echo "/usr/lib/libsys-assert.so" >> /etc/ld.so.preload
	chmod 644 /etc/ld.so.preload
fi

%files
%manifest %{name}.manifest
/opt/etc/.debugmode
%{_libdir}/libsys-assert.so
/usr/share/license/%{name}
%{_libdir}/systemd/system/tizen-debug-on.service
%{_libdir}/systemd/system/tizen-debug-off.service
%{_libdir}/systemd/system/sysinit.target.wants/tizen-debug-on.service
%{_libdir}/systemd/system/sysinit.target.wants/tizen-debug-off.service
