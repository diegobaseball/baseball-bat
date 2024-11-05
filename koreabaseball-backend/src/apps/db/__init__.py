from config import (
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DB,
)

from uuid import UUID, uuid4
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from sqlmodel import Field, SQLModel, create_engine, Session


class Users(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    uuid: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str
    password: str
    name: str
    email: str
    birthdate: str
    gender: str
    status: str
    stands: str | None
    throws: str | None
    picture: str | None


class Tokens(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    uuid: UUID = Field(primary_key=True)
    username: str
    access_token: str
    refresh_token: str
    status: bool
    created_date: datetime = Field(
        default_factory=datetime.now,
    )


class Players(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    uuid: UUID | None = Field(primary_key=True, default=None)
    is_registered_player: bool
    name: str
    deep_squat: str
    hurdle_step: str
    inline_lunge: str
    ankle_clearing_pian: str
    ankle_clearing_mobility: str
    shoulder_mobility: str
    active_straight_leg_raise: str
    trunk_stability_pushup: str
    rotary_stability: str


class GraphSensorData(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    uuid: UUID | None = Field(primary_key=True, default=None)
    is_registered_player: bool
    frame: int
    frequency: int
    sec: float
    utc_time: datetime


class Metrics(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    uuid: UUID | None = Field(primary_key=True, default=None)
    is_registered_player: bool
    name: str
    date_time: datetime
    sequence_transition: str
    sequence_deceleration: str
    spine_stability: float
    chest_delay: float
    chest_quickness: float
    pelvis_quickness: float


class MetricsAggregate(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    uuid: UUID | None = Field(primary_key=True, default=None)
    is_registered_player: bool
    name: str
    date_time: datetime
    sequence_transition: str
    sequence_deceleration: str
    spine_stability: float
    chest_delay: float
    chest_quickness: float
    pelvis_quickness: float


class BlastMotionData(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    uuid: UUID | None = Field(primary_key=True, default=None)
    is_registered_player: bool
    date: datetime
    equipment: str
    handedness: str
    swing_details: str
    plane_score: int
    connection_score: int
    rotation_score: int
    bat_speed_mph: float
    rotational_acceleration_g: float
    on_plane_efficiency_p: int
    attack_angle_deg: int
    early_connection_deg: int
    connection_at_impact_deg: int
    vertical_bat_angle_deg: int
    power_kw: float
    time_to_contact_sec: float
    peak_hand_speed_mph: float
    exit_velocity_mph: float
    launch_angle_deg: float
    estimated_distance_feet: float
    player: str


class HitTraxData(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    uuid: UUID | None = Field(primary_key=True, default=None)
    is_registered_player: bool
    no: int
    ab: int
    player: str
    date: datetime
    timestamp: timedelta
    release_speed: float
    strike_zone: str
    pitch_type: str
    launch_speed: float
    launch_angle: float
    hit_distance_sc: int
    pa_result: str
    type: str
    horiz_angle: float
    pts: int
    hand_speed: float | None
    bv: float | None
    trigger_to_impact: float | None
    aa: float | None
    impact_momentum: float | None
    strike_zone_bottom: float
    strike_zone_top: float
    strike_zone_width: float
    vertical_distance: float
    horizontal_distance: float
    poix: float | None
    poiy: float | None
    poiz: float | None
    spray_chart_x: float | None
    spray_chart_z: float | None
    fielded_x: float | None
    fielded_z: float | None
    bat_material: str
    user: str
    pitch_angle: float
    batting: str
    level: str
    opposing_player: str
    _tag: str
    player: str
    handspeed: float
    bv: float
    triggertoimpact: float
    aa: float
    impactmomentum: float
    tag: str


class FMSProfile(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    uuid: UUID | None = Field(primary_key=True, default=None)
    is_registered_player: bool
    tibia_height: int
    hand_length: int
    date: datetime


class FMSMeasurement(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    uuid: UUID | None = Field(primary_key=True, default=None)
    is_registered_player: bool
    date: timedelta
    deepsquat: int
    hurdlestep_r: int
    hurdlestep_l: int
    inlineLunge_r: int
    inlineLunge_l: int
    ankleclearingpian_r: int
    ankleclearingpian_l: int
    ankleclearingmobility_r: int
    ankleclearingmobility_l: int
    ankleclearingmobility_r_ryg: str
    ankleclearingmobility_l_ryg: str
    shouldermobility_r: int
    shoulderMobility_l: int
    shoulderclearing_r: int
    shoulderclearing_l: int
    activestraightlegraise_r: int
    activestraightlegraise_l: int
    trunkstabilitypushup: int
    extensionclearing: int
    rotarystability_r: int
    rotarystability_l: int
    flexionclearing: int


class FMSDailyTotalScore(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    uuid: UUID | None = Field(primary_key=True, default=None)
    is_registered_player: bool
    date: timedelta
    deepsquat: int
    hurdlestep_r: int
    hurdlestep_l: int
    inlineLunge_r: int
    inlineLunge_l: int
    ankleclearingpian_r: int
    ankleclearingpian_l: int
    ankleclearingmobility_r: int
    ankleclearingmobility_l: int
    ankleclearingmobility_r_ryg: str
    ankleclearingmobility_l_ryg: str
    shouldermobility_r: int
    shoulderMobility_l: int
    shoulderclearing_r: int
    shoulderclearing_l: int
    activestraightlegraise_r: int
    activestraightlegraise_l: int
    trunkstabilitypushup: int
    extensionclearing: int
    rotarystability_r: int
    rotarystability_l: int
    flexionclearing: int
    rotalscreenscore: int


class OnBaseballUnivHittingScreen(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    uuid: UUID | None = Field(primary_key=True, default=None)
    is_registered_player: bool
    date: timedelta
    toetouchwidthl: bool
    toetouchwidthr: bool
    hipholdstablel: bool
    hipholdstabler: bool
    hipflex45l: str
    hipflex45r: str
    trunkrot45l: str
    trunkrot45r: str
    trunkrotheadl: bool
    trunkrotheadr: bool
    pelvictiltstance: str
    pelvictiltrange: str
    pelvictiltdegree: str
    pelvicrotnoshoulderl: bool
    pelvicrotnoshoulderr: bool
    pelvicrotshoulderl: bool
    pelvicrotshoulderr: bool
    pelvicmovementl: bool
    pelvicmovementr: bool
    shouldeelbowto2ndbasel: str
    shouldeelbowto2ndbaser: str
    separateelbowaboveshoulderl: bool
    separateelbowaboveshoulderr: bool
    separatehandpushl: str
    separatehandpushr: str
    fixedangleupperhand: str
    fixedangleoppositehand: str
    hitchpronation80l: bool
    hitchpronation80r: bool
    hitchsupination80l: bool
    hitchsupination80r: bool
    sidesteptouchl: str
    sidesteptouchr: str
    squatarmsforward: bool
    squatarmlower: bool
    ankleshakesittingl: str
    ankleshakesittingr: str
    ankleshakefistl: str
    ankleshakefistr: str


postgresql_url = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(postgresql_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
