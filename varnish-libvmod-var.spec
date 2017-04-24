#
# Conditional build:
%bcond_without	tests		# build without tests

%define	vmod	var
Summary:	Variable support VMOD
Name:		varnish-libvmod-%{vmod}
Version:	0.1
Release:	2
License:	BSD
Group:		Daemons
Source0:	https://github.com/varnish/libvmod-var/archive/3.0/%{vmod}-%{version}.tar.gz
# Source0-md5:	5215b83ff6debb9c5bae01cd21f4e6e0
URL:		https://github.com/varnish/libvmod-var
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	python-docutils
BuildRequires:	varnish-source
%{?with_tests:BuildRequires:	varnish}
%requires_eq_to varnish varnish-source
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		vmoddir	%(pkg-config --variable=vmoddir varnishapi || echo ERROR)

%description
This VMOD implements basic variable in VCL. Well. It's more of an
association list with support for strings, ints and reals.

There are methods to get and set each type.

Global variables have a lifespan that extends across requests and
VCLs, for as long as the vmod is loaded. Non-globals are local to a
single request.

%prep
%setup -qc
mv libvmod-%{vmod}-*/* .

%build
%{__aclocal} -I m4
%{__libtoolize}
%{__autoheader}
%{__automake}
%{__autoconf}

VARNISHSRC=$(pkg-config --variable=srcdir varnishapi)
%configure \
	VARNISHSRC=$VARNISHSRC \
	VMODDIR=%{vmoddir} \
	--disable-static

%{__make}
%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/varnish/vmods/libvmod_%{vmod}.la
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/libvmod-%{vmod}
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man3/vmod_example.3*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README LICENSE
%attr(755,root,root) %{vmoddir}/libvmod_%{vmod}.so
