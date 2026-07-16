import { useEffect } from 'react'
import { Link, Navigate, useParams } from 'react-router-dom'
import Reveal from '../components/Reveal'
import { PRODUCTS, CONTACT_EMAIL } from '../data/products'

export default function ProductPage() {
  const { slug } = useParams()
  const product = PRODUCTS.find((p) => p.slug === slug)

  useEffect(() => {
    document.title = product ? `${product.name} · Norvia Solutions` : 'Norvia Solutions'
    return () => {
      document.title = 'Norvia Solutions'
    }
  }, [product])

  if (!product) {
    return <Navigate to="/" replace />
  }

  return (
    <main style={{ '--hue': product.hue } as React.CSSProperties}>
      <section className="prod-hero wrap">
        <Link className="back-link" to="/#produtos">
          ← Todos os produtos
        </Link>
        <p className="tag">{product.tag}</p>
        <h1>{product.name}</h1>
        <p className="lead">{product.summary}</p>
        <div className="prod-meta">
          <span>{product.platform}</span>
          <span>{product.tech}</span>
        </div>
        <div className="hero-ctas">
          {product.links.length > 0 ? (
            product.links.map((link, i) => (
              <a
                key={link.url}
                className={`btn ${i === 0 ? 'btn-gold' : 'btn-ghost'}`}
                href={link.url}
                target="_blank"
                rel="noopener noreferrer"
              >
                {link.label} ↗
              </a>
            ))
          ) : (
            <a className="btn btn-gold" href={`mailto:${CONTACT_EMAIL}`}>
              Saiba mais pelo e-mail
            </a>
          )}
        </div>
      </section>

      <section className="wrap prod-body">
        <Reveal className="txt">
          <p className="eyebrow">Sobre o produto</p>
          {product.description.map((paragraph) => (
            <p key={paragraph}>{paragraph}</p>
          ))}
        </Reveal>
        <Reveal>
          <div className="features">
            {product.features.map((f) => (
              <div className="feature" key={f.title}>
                <h4>{f.title}</h4>
                <p>{f.text}</p>
              </div>
            ))}
          </div>
        </Reveal>
      </section>
    </main>
  )
}
