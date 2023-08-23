import ReservationCard from "./ReservationCard"
import { useEffect, useState, useContext } from "react"
import { UserContext } from '../context/user'

function Home({  }) {
    const { user, setUser } = useContext(UserContext)
    const [ reservations, setReservations ] = useState([])

    useEffect(()=>{
        document.title = 'Flatlines | Home'
        fetch("/authorized")
            .then( r => {
            if (r.ok) {
              r.json().then( user => {
                setUser(user) 
                setReservations(user.reservations)
                }) } }) 
    },[])

    const renderedReservations = reservations.map( reservation => 
        <ReservationCard
            key = {reservation.id}
            reservationId = {reservation.id}
            flightId = {reservation.flight_id}
            seat = {reservation.seat}
            confNum = {reservation.conf_number}
    />)

    if (!user) return <h1>loading</h1>
    return(
        <div>
            {renderedReservations}
        </div>
    )
}

export default Home