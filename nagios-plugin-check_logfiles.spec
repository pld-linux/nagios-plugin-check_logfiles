%define		plugin	check_logfiles
%include	/usr/lib/rpm/macros.perl
BuildRequires:	rpm-perlprov >= 4.1-13
Summary:	Check log files for specific patterns
Name:		nagios-plugin-%{plugin}
Version:	2.4.1.9
Release:	0.1
License:	BSD
Group:		Networking
URL:		http://www.consol.com/opensource/nagios/check-logfiles
Source0:	http://www.consol.com/fileadmin/opensource/Nagios/check_logfiles-%{version}.tar.gz
# Source0-md5:	fc2b0d394626eb715643cdbbaf13ba69
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/nagios/plugins
%define		plugindir	%{_prefix}/lib/nagios/plugins

# just to fool configure, nothing arch specific actually
%define		_target_platform	%{_host_cpu}-%{_vendor}-%{_os}

%description
check_logfiles is a Plugin for Nagios which scans log files for
specific patterns.

%prep
%setup -q -n %{plugin}-%{version}

cat > nagios.cfg <<'EOF'
# Usage:
# %{plugin}
define command {
	command_name    %{plugin}
	command_line    %{plugindir}/%{plugin} $ARG1$
}
EOF

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
	--with-trusted-path="/bin:/sbin:/usr/bin:/usr/sbin" \
	--with-nagios-user=nagios \
	--with-nagios-group=nagios \
	--libexec=%{plugindir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -a nagios.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{plugin}.cfg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README ChangeLog TODO
%attr(755,root,root) %{plugindir}/%{plugin}
