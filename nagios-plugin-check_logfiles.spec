%define		plugin	check_logfiles
Summary:	Check log files for specific patterns
Name:		nagios-plugin-%{plugin}
Version:	3.8.1.4
Release:	1
License:	GPL v2
Group:		Applications
Source0:	https://labs.consol.de/assets/downloads/nagios/%{plugin}-%{version}.tar.gz
# Source0-md5:	cc64759534638d17fae051cac8a705fa
Source1:	check_logfiles.cfg
URL:		https://labs.consol.de/nagios/check_logfiles/
BuildRequires:	rpm-perlprov >= 4.1-13
Requires:	nagios-core
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir		/etc/nagios/plugins
%define		plugindir		%{_prefix}/lib/nagios/plugins
%define		trusted_path	/bin:/sbin:/usr/bin:/usr/sbin

# just to fool configure, nothing arch specific actually
%if "%{_host_cpu}" != "x32"
%define		_target_platform	%{_host}
%endif

%description
check_logfiles is a Plugin for Nagios which scans log files for
specific patterns.

%prep
%setup -q -n %{plugin}-%{version}

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--with-perl=%{__perl} \
	--with-gzip=%{__gzip} \
	--with-seekfiles-dir=/tmp \
	--with-protocols-dir=/tmp \
	--with-trusted-path="%{trusted_path}" \
	--with-nagios-user=nagios \
	--with-nagios-group=nagios \
	--libexec=%{plugindir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{plugin}.cfg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README ChangeLog TODO
%attr(640,root,nagios) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{plugin}.cfg
%attr(755,root,root) %{plugindir}/%{plugin}
