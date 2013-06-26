Name:       sys-assert
Summary:    libsys-assert (shared object).
Version:    0.3.3
Release:    5
Group:      Framework/system
License:    Apache License, Version 2.0
Source0:    %{name}-%{version}.tar.gz

BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libunwind)
BuildRequires:  cmake
Requires(post): coreutils
Requires(post): smack-utils

%description
libsys-assert (shared object).

%prep
%setup -q

%build
export CFLAGS+=" -fPIC -lunwind"
%ifarch %{arm}
    export CFLAGS+=" -DTARGET"
%endif

%cmake .
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install
mkdir -p %{buildroot}/usr/share/license
cp LICENSE.APLv2 %{buildroot}/usr/share/license/%{name}

%post
/sbin/ldconfig
mkdir -p /opt/share/crash/info
chown root:crash /opt/share/crash/info
chmod 775 /opt/share/crash/info

chown root:crash /opt/share/crash
chmod 750 /opt/share/crash

if [ -f %{_libdir}/rpm-plugins/msm.so ]; then
	find /opt/share/crash -print0 | xargs -0 chsmack -a 'sys-assert::core'
	find /opt/share/crash -type d -print0 | xargs -0 chsmack -t
fi

if [ ! -d /.build ]; then
	echo "/usr/lib/libsys-assert.so" >> /etc/ld.so.preload
	chmod 644 /etc/ld.so.preload
fi

%files
%manifest sys-assert.manifest
%{_bindir}/coredumpctrl.sh
%{_libdir}/libsys-assert.so
/opt/etc/.debugmode
/usr/share/license/%{name}
/usr/lib/sysctl.d/sys-assert.conf
