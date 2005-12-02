#
# TODO:
#	- init script should be fixed
#	- run as uid>0 !
#
Summary:	Edna - streaming server
Summary(pl):	Edna - serwer strumieni
Name:		edna
Version:	0.5
Release:	1
License:	GPL
Group:		Applications/Sound
Source0:	http://edna.sourceforge.net/%{name}-%{version}.tar.gz
# Source0-md5:	ec3d46b25fa582b78db7c32acf78da47
Source1:	%{name}.init
URL:		http://edna.sourceforge.net/
BuildRequires:	rpm-pythonprov
Requires:	rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	python
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Edna allows you to access your MP3 collection from any networked
computer. This software streams your MP3s via HTTP to any MP3 player
that supports playing off a remote connection (e.g. Winamp, FreeAmp,
Sonique, XMMS). Edna supports Ogg files either.

%description -l pl
Edna umo¿liwia dostêp do kolekcji MP3 z dowolnego komputera maj±cego
dostêp do sieci. Ten program wysy³a strumieñ MP3 po HTTP do dowolnego
odtwarzacza MP3 obs³uguj±cego odtwarzanie przez po³±czenie sieciowe
(jak Winamp, FreeAmp, Sonique, XMMS). Edna obs³uguje tak¿e pliki Ogg.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -d $RPM_BUILD_ROOT%{_sysconfdir}/edna

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	LIBDIR=$RPM_BUILD_ROOT%{_datadir}/edna

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/edna
install edna.conf $RPM_BUILD_ROOT%{_sysconfdir}/edna
ln -sf %{_datadir}/edna/templates $RPM_BUILD_ROOT%{_sysconfdir}/edna/templates

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add edna
if [ -f /var/lock/subsys/edna ]; then
	/etc/rc.d/init.d/edna restart >&2
else
	echo "Run '/etc/rc.d/init.d/edna start' to start edna daemon." >&2
fi

%preun
if [ "$1" = "0" ] ; then
	if [ -f /var/lock/subsys/edna ]; then
		/etc/rc.d/init.d/edna stop >&2
	fi
	/sbin/chkconfig --del edna >&2
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog README
%attr(755,root,root) %{_bindir}/edna
%attr(754,root,root) /etc/rc.d/init.d/edna
%dir %{_sysconfdir}/edna
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/edna/edna.conf
%{_sysconfdir}/edna/templates
%{_datadir}/%{name}
