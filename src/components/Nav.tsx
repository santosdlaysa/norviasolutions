import { Link } from 'react-router-dom'

const LINKS = [
  { label: 'Produtos', to: '/#produtos' },
  { label: 'Serviços', to: '/#servicos' },
  { label: 'Sobre', to: '/#sobre' },
  { label: 'Contato', to: '/#contato' },
]

export default function Nav() {
  return (
    <header className="nav">
      <div className="wrap nav-inner">
        <Link className="brand" to="/">
          <span className="dot" />
          norvia<span className="sol">solutions</span>
        </Link>
        <nav className="links" aria-label="Navegação principal">
          {LINKS.map((link) => (
            <Link key={link.to} to={link.to}>
              {link.label}
            </Link>
          ))}
        </nav>
        <Link className="nav-cta" to="/#contato">
          Fale conosco
        </Link>
      </div>
    </header>
  )
}
